import importlib
import json
import os
import re
import shutil
import subprocess
import time
from types import ModuleType
from typing import List, Dict, Any, Tuple
from urllib.parse import unquote

import requests

from aicrowd.utils.jupyter import is_google_colab_env, mount_google_drive


def read_notebook(file_path: str) -> Dict[str, Any]:
    with open(file_path) as fp:
        nb = json.load(fp)
    return nb


def write_notebook(file_path: str, nb: Dict[str, Any]):
    with open(file_path, "w") as fp:
        json.dump(nb, fp)


def delete_expressions_from_notebook(
    expressions: List[str], file_path: str
) -> Dict[str, Any]:
    """
    Delete code lines from the notebook that match the regular expressions

    Args:
        expressions: List of regular expressions to match
        file_path: Path to the notebook
    """
    nb = read_notebook(file_path)

    # TODO: Duplicated code, refactor
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


def convert_timestamp_to_epoch(timestamp: str) -> float:
    pattern = "%Y-%m-%dT%H:%M:%S.%fZ"
    return time.mktime(time.strptime(timestamp, pattern))


def get_default_jupyter_api_session_host() -> str:
    if is_google_colab_env():
        return "http://172.28.0.2:9000"
    return "http://127.0.0.1:8888"


def get_latest_jupyter_session() -> Dict[str, Any]:
    proxies = {"http": None, "https": None}
    (
        auto_detected_jupyter_host,
        auto_detected_jupyter_token,
    ) = get_jupyter_server_endpoint()
    jupyter_notebook_host = os.getenv("JUPYTER_NB_HOST", auto_detected_jupyter_host)
    response = requests.get(
        os.path.join(jupyter_notebook_host, "api/sessions"),
        proxies=proxies,
        headers={"Authorization": f"token {auto_detected_jupyter_token}"},
    )
    if not response.ok:
        raise requests.exceptions.HTTPError(
            f"Got invalid response from Jupyter: {response.text}"
        )
    sessions = response.json()
    latest_session = sorted(
        sessions,
        reverse=True,
        key=lambda x: convert_timestamp_to_epoch(
            x.get("kernel", {}).get("last_activity", -1)
        ),
    )[0]
    return latest_session


def get_notebook_path():
    if is_google_colab_env():
        return get_colab_notebook_path()
    else:
        return get_jupyter_notebook_path()


def get_jupyter_notebook_path():
    return os.path.join(os.getcwd(), get_latest_jupyter_session()["name"])


def get_colab_notebook_path():
    mount_path = mount_google_drive()
    return os.path.join(
        mount_path,
        "MyDrive/Colab Notebooks",
        unquote(get_latest_jupyter_session()["name"]),
    )


def bundle_notebook(submission_dir: str, notebook_name: str = None):
    if is_google_colab_env():
        raise NotImplementedError("Google colab submissions are not ready yet")
    else:
        bundle_original_jupyter_notebook(submission_dir, notebook_name)


def bundle_original_jupyter_notebook(submission_dir: str, notebook_name: str = None):
    submission_dir = submission_dir.replace(".zip", "")
    if notebook_name is None:
        notebook_name = get_jupyter_notebook_path()
    shutil.copy(notebook_name, os.path.join(submission_dir, "original_notebook.ipynb"))


def get_runtime_language() -> Tuple[str, str]:
    kernel = get_latest_jupyter_session()["kernel"]["name"]
    if kernel == "ir":
        return "r", kernel
    if kernel.startswith("python"):
        return "python", kernel


def write_aicrowd_config(submission_dir: str):
    language, kernel = get_runtime_language()
    config = {
        "language": language,
        "kernel": kernel,  # we do not use this value, it's added only for debugging
    }
    with open(os.path.join(submission_dir, "aicrowd.json"), "w") as fp:
        json.dump(config, fp)


def get_kernel_from_language(language: str) -> str:
    if language.lower() == "python":
        if is_google_colab_env():
            return "python3"
        return "python"
    if language.lower() == "r":
        return "ir"
    raise NotImplementedError("Unsupported language")


def import_module(module_name: str) -> ModuleType:
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pass


def get_jupyter_server_endpoint() -> Tuple[str, str]:
    """
    Returns the jupyter server endpoint along with the token

    Returns:
        Jupyter server endpoint and token
    """
    notebook_server = import_module("jupyter_server.serverapp")
    if not notebook_server:
        print("No jupyter lab module found. Using jupyter notebook.")
        notebook_server = import_module("notebook.notebookapp")

    if not notebook_server:
        print("No jupyter notebook module found. Using default values.")
        return get_default_jupyter_api_session_host(), ""

    session_list = list(notebook_server.list_running_servers())
    if len(session_list) > 1:
        print("WARNING: Got more than 1 jupyter server, selecting the latest session")
    if len(session_list) == 0:
        raise RuntimeError(
            "No jupyter server found. Did you start your jupyter server?"
        )
    return session_list[-1]["url"], session_list[-1]["token"]
