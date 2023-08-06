"""
Submission related tasks
"""
import json
import logging
import os
import re
import shutil
from pathlib import Path
from typing import Tuple, List, Dict, Any

import requests
from urllib.parse import unquote
from requests_toolbelt import MultipartEncoderMonitor
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table

# pylint: disable=unused-import
from aicrowd.challenge.helpers import must_get_api_key, parse_cli_challenge

# pylint: enable=unused-import
from aicrowd.constants import RAILS_API_ENDPOINT, RAILS_HOST
from aicrowd.utils.jupyter import (
    is_jupyter,
    is_google_colab_env,
    mount_google_drive,
    get_aicrowd_config,
)
from aicrowd.utils.utils import zip_fs_path
from aicrowd.submission.exceptions import (
    SubmissionFileException,
    SubmissionUploadException,
)


def calculate_min_table_width(table: Table):
    """
    Calculates minumum width needed to display table text properly

    Args:
        table: rich table
    """
    width = sum(table._calculate_column_widths(Console(), 200)) + table._extra_width
    term_width = shutil.get_terminal_size().columns
    return max(width, term_width)


def get_upload_details(challenge_slug: str, api_key: str) -> Tuple[dict, bool]:
    """
    Contacts AIcrowd website for getting presigned url for uploading

    Args:
        challenge_slug: challenge slug
        api_key: AIcrowd API Key

    Returns:
        the data and whether the request was successful or not
    """
    log = logging.getLogger()

    r = requests.get(
        f"{RAILS_API_ENDPOINT}/submissions",
        params={"challenge_id": challenge_slug},
        headers={"Authorization": f"Token token={api_key}"},
        allow_redirects=False,
    )

    # temporary hack until /api stops redirecting
    if r.status_code // 100 == 3:
        redirected_to = r.headers["Location"]
        expected_redirect = f"https://{RAILS_HOST}"

        if redirected_to.startswith(expected_redirect):
            redirected_to = redirected_to[len(expected_redirect) :]
        else:
            # got redirected to a weird place
            logging.error(
                "Unexpected redirect location: %s\nExpected %s",
                redirected_to,
                expected_redirect,
            )
            return {}, False

        challenge_problem = re.match(
            r"/challenges/([^/]*)/problems/([^/]*)/.*", redirected_to
        ).groups()
        logging.info("[metachallenge?] Got redirected to %s", redirected_to)

        # inform caller about meta_challenge
        return {
            "meta_challenge": True,
            "meta_challenge_id": challenge_problem[0],
            "challenge_id": challenge_problem[1],
        }, True

    try:
        resp = r.json()

        if not r.ok or not resp.get("success"):
            log.error(
                "Request to API failed\nReason: %s\nMessage: %s", r.reason, r.text
            )
            return resp, False

        return resp.get("data"), True
    except Exception as e:
        log.error("Error while extracting details: %s", e)
        return {}, False


class S3Uploader:
    """
    Upload files to s3 with progress bar
    """

    def __init__(self, host: str, fields: dict, file_path: str):
        """
        Args:
            host: s3 host to upload to
            fields: s3 related fields
            file_path: the file to upload
        """
        self.host = host
        self.fields = fields

        file_path = Path(file_path)

        self.file_name = file_path.name
        self.file_size = file_path.stat().st_size

        self.fields["key"] = self.fields["key"].replace("${filename}", self.file_name)
        self.fields["file"] = (self.file_name, file_path.open("rb"))

        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[file_name]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )
        self.progress.console.is_jupyter = is_jupyter()
        self.task_id = self.progress.add_task(
            "upload", file_name=self.file_name, start=False, total=self.file_size
        )

    def track_progress(self, monitor: MultipartEncoderMonitor):
        """
        shows progress bar showing how much has been uploaded

        Args:
            monitor: requests_toolbelt Monitor
        """
        self.progress.update(self.task_id, completed=monitor.bytes_read, refresh=True)

    def upload(self):
        """
        upload file to s3
        """
        self.progress.start_task(self.task_id)
        m = MultipartEncoderMonitor.from_fields(
            self.fields, callback=self.track_progress
        )

        with self.progress:
            return (
                requests.post(
                    self.host, data=m, headers={"Content-Type": m.content_type}
                ),
                self.fields["key"],
            )


def upload_submission(host: str, fields: dict, file_path: str) -> str:
    """
    uploads a file to s3 using presigned url details

    Args:
        host: s3 host to upload to
        fields: s3 related keys
        file_path: the file to be uploaded

    Returns:
        whether it was successful or not
    """
    log = logging.getLogger()

    r, s3_key = S3Uploader(host, fields, file_path).upload()

    if not r.ok:
        log.error(
            "Couldn't upload file to s3\nReason: %s\nMessage: %s", r.reason, r.text
        )
        return None

    return s3_key


def notify_rails_upload(
    challenge_slug: str,
    submitted_url: str,
    api_key: str,
    description: str,
    problem_slug: str = None,
) -> dict:
    """
    notify rails about the uploaded file on s3

    Args:
        challenge_slug: challenge slug
        submitted_url: the url to which the submitted file was uploaded to
        description: submission description
        problem_slug: Used when submitting to a meta challenge

    Returns:
        submission details from AIcrowd API
    """
    log = logging.getLogger()

    if problem_slug is None:
        payload = {"challenge_id": challenge_slug}
    else:
        payload = {"meta_challenge_id": challenge_slug, "challenge_id": problem_slug}

    payload.update(
        {
            "description": description,
            "submission_files": [{"submission_file_s3_key": submitted_url}],
        }
    )

    r = requests.post(
        f"{RAILS_API_ENDPOINT}/submissions",
        json=payload,
        headers={"Authorization": f"Token token={api_key}"},
    )

    if not r.ok:
        log.error("Request to API failed\nReason: %s\nMessage: %s", r.reason, r.text)
        return {}

    try:
        return r.json()
    except Exception as e:
        log.error("Couldn't json-decode rails response")
        return {}


def print_submission_links(challenge_slug: str, problem_slug: str, submission_id: int):
    """
    prints helpful links related to the submission

    Args:
        challenge_slug: challenge slug
        problem_slug: when submitting to a meta challenge
        submission_id: rails submission id
    """
    if submission_id is None:
        return

    if problem_slug:
        challenge_url = (
            f"https://{RAILS_HOST}/challenges/{challenge_slug}/problems/{problem_slug}"
        )
    else:
        challenge_url = f"https://{RAILS_HOST}/challenges/{challenge_slug}"

    submission_base_url = f"{challenge_url}/submissions"

    table = Table(title="Important links", show_header=False, leading=1, box=box.SQUARE)
    table.add_column(justify="right")
    table.add_column(overflow="fold")

    table.add_row("This submission", f"{submission_base_url}/{submission_id}")
    table.add_row("All submissions", f"{submission_base_url}?my_submissions=true")
    table.add_row("Leaderboard", f"{challenge_url}/leaderboards")
    table.add_row(
        "Discussion forum", f"https://discourse.aicrowd.com/c/{challenge_slug}"
    )
    table.add_row("Challenge page", f"{challenge_url}")

    width = calculate_min_table_width(table)

    console = Console(width=width)
    table.min_width = width
    console.print(Panel("[bold]Successfully submitted!"), justify="center")
    console.print(table)


def submit_file(
    challenge_slug: str,
    file_path: str,
    description: str,
    api_key: str,
    print_links: bool,
) -> dict:
    """
    Submits a file given it's path and challenge_slug with given description

    Args:
        challenge_slug: challenge slug
        file_path: path to the file to be uploaded
        description: description for the submission
        api_key: AIcrowd API Key
        print_links: should helpful links be printed?

    Returns:
        a message from AIcrowd API
    """
    log = logging.getLogger()
    problem_slug = None

    if not Path(file_path).is_file():
        raise SubmissionFileException(f"Bad file {file_path}")

    s3_presigned_details, success = get_upload_details(challenge_slug, api_key)

    if s3_presigned_details.get("meta_challenge"):
        challenge_slug = s3_presigned_details.get("meta_challenge_id")
        problem_slug = s3_presigned_details.get("challenge_id")

        s3_presigned_details, success = get_upload_details(challenge_slug, api_key)

    if not success:
        log.error(
            "Error in getting presigned url for s3 upload: %s",
            s3_presigned_details.get("message"),
        )
        raise SubmissionUploadException(s3_presigned_details.get("message"))

    s3_key = upload_submission(
        s3_presigned_details["url"], s3_presigned_details["fields"], file_path
    )
    if s3_key is None:
        raise SubmissionUploadException(
            "Couldn't submit file. Please recheck the files and details provided"
        )

    response = notify_rails_upload(
        challenge_slug, s3_key, api_key, description, problem_slug
    )
    if not response.get("success"):
        raise SubmissionUploadException(
            response.get("message", "Error in notifying rails about the uploaded file")
        )

    if print_links:
        print_submission_links(
            challenge_slug, problem_slug, response.get("data", {}).get("submission_id")
        )

    return response.get("data")


def bundle_notebook_submission() -> str:
    """
    Bundle submission files along with the colab/jupyter notebook

    Any additional files in `AIcrowdConfig.ASSETS_DIR` will be added to the
    submission zip file.

    Returns:
        Path to the submission zip file
    """
    console = Console()

    if not is_jupyter():
        raise EnvironmentError("Not running in jupyter notebook")

    config = get_aicrowd_config()
    assets_dir = getattr(config, "ASSETS_DIR", None)
    if assets_dir is None:
        console.print("WARNING: No assets directory provided", style="bold red")

    target_zip_path = "submission"
    zip_assets(assets_dir, target_zip_path)

    if is_google_colab_env():
        zip_colab_notebook(target_zip_path)
    else:
        zip_jupyter_notebook(target_zip_path)

    return target_zip_path + ".zip"


def zip_assets(assets_dir: str, target_zip_path: str):
    """
    Zip the files under assets directory

    Args:
        assets_dir: Directory containing submission assets
        target_zip_path: Path to zip file to add the entries to
    """
    console = Console()
    if not os.path.exists(assets_dir):
        os.mkdir(assets_dir)
        console.print("WARNING: Assets dir is empty", style="bold red")
    zip_fs_path(assets_dir, target_zip_path)


def zip_jupyter_notebook(
    target_zip_path: str, submission_notebook_path: str = "submission.ipynb"
):
    """
    Add the jupyter notebook to the submission zip file

    The notebook will be available on the local file system which won't be
    the case colab notebook. So this should be used with colab notebook.

    Args:
        target_zip_path: Path to zip file to add the notebook to
        submission_notebook_path: Path to the submission notebook
    """
    notebook_path = get_jupyter_notebook_path()
    cleaned_nb = pop_source_line(
        os.path.join(notebook_path),
        ['API_KEY(\s+)?=(\s+)?".+"'],
    )
    with open(submission_notebook_path, "w") as fp:
        json.dump(cleaned_nb, fp)
    zip_fs_path(
        submission_notebook_path,
        target_zip_path,
    )


def get_jupyter_notebook_path():
    """
    Get the path to jupyter notebook from the sessions endpoint

    This assumes that jupyter is running without authentication on port 8888

    Returns:
        Path to the jupyter notebook
    """
    # TODO: Dynamically detect the endpoint
    # TODO: Support with notebooks with auth
    proxies = {
        "http": None,
        "https": None,
    }
    session_info = requests.get(
        "http://localhost:8888/api/sessions", proxies=proxies
    ).json()
    check_session_count(session_info)
    return unquote(session_info[0]["path"])


def zip_colab_notebook(target_zip_path: str):
    """
    Add the colab notebook to the submission zip file

    We do not have direct access to the colab notebook on the local FS. So,
    we mount the user's Google Drive and copy the notebook from there.

    Args:
        target_zip_path: Path to zip file to add the notebook to
    """
    mount_path = mount_google_drive()
    submission_notebook_path = "submission.ipynb"
    cleaned_nb = pop_source_line(
        os.path.join(
            mount_path, "My Drive", "Colab Notebooks", get_colab_notebook_name()
        ),
        ['API_KEY(\s+)?=(\s+)?".+"'],
    )
    with open(submission_notebook_path, "w") as fp:
        json.dump(cleaned_nb, fp)
    zip_fs_path(
        submission_notebook_path,
        target_zip_path,
    )


def pop_source_line(file_path: str, expressions: List[str]) -> Dict[str, Any]:
    """Remove certain code lines matching given regular expressions from the
    notebook

    Args:
        file_path: Submission notebook path
        expressions: List of regular expressions to match

    Returns:
        New notebook with matched lines removed
    """
    with open(file_path) as fp:
        nb = json.load(fp)

    for _cell in nb["cells"]:
        # Match the lines only in code blocks
        if _cell["cell_type"] == "code":
            source_code = []
            for _code_line in _cell["source"]:
                matched = False
                for _expr in expressions:
                    if re.search(_expr, _code_line):
                        matched = True
                        break
                if not matched:
                    source_code.append(_code_line)
            _cell["source"] = source_code
    return nb


def get_colab_notebook_name() -> str:
    """Get name of the current notebook

    Returns:
        Name of the current colab notebook
    """
    sesssion_info = requests.get("http://172.28.0.2:9000/api/sessions").json()
    check_session_count(sesssion_info)
    return unquote(sesssion_info[0]["name"])


def check_session_count(sesssion_info):
    if len(sesssion_info) == 0:
        raise EnvironmentError("Please start the notebook with a kernel")
    if len(sesssion_info) > 1:
        raise EnvironmentError(
            "Found more than one kernel running. Please close other notebooks and kernels and try again."
        )


def delete_and_copy_dir(src: str, dst: str):
    """
    Delete if the src exists and copy files from src to dst

    Args:
        src: Source path
        dst: Destination path
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
