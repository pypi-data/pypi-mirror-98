import json
import os
import shutil
import subprocess

from aicrowd.utils.jupyter import execute_command, is_google_colab_env
from aicrowd.notebook.clean import clean_notebook
from aicrowd.notebook.helpers import (
    bundle_notebook,
    get_jupyter_notebook_path,
    write_aicrowd_config,
    get_kernel_from_language,
    get_notebook_path,
)
from aicrowd.notebook.split import split_notebook
from aicrowd.submission import create as submit_to_aicrowd

SUBMISSION_DIR = os.path.join(os.getcwd(), "submission")


def verify_submission():
    print("Validating the submission...")
    if not os.path.exists(SUBMISSION_DIR):
        raise FileNotFoundError("Please bundle the submission before local evaluation")
    with open(os.path.join(SUBMISSION_DIR, "aicrowd.json")) as fp:
        config = json.load(fp)
    nbconvert_cmd = "jupyter nbconvert --to notebook --ExecutePreprocessor.kernel_name={} --execute {}/{}"
    kernel = get_kernel_from_language(config["language"])
    for notebook in ["install.ipynb", "predict.ipynb"]:
        print(f"Executing {notebook}...")
        if execute_command(nbconvert_cmd.format(kernel, SUBMISSION_DIR, notebook)) != 0:
            raise RuntimeError(f"{notebook} failed to execute")


def bundle_submission(
    assets_dir: str,
    submission_zip_path: str = "submission.zip",
    notebook_name: str = None,
):
    # Make sure that assets dir is a direct child of current dir
    if os.path.basename(assets_dir) != assets_dir:
        raise NameError(
            "Assets directory should be a direct part of the current directory"
        )
    if not os.path.exists(assets_dir):
        print(f"WARNING: No assets directory at {assets_dir}... Creating one...")
        os.mkdir(assets_dir)
    if os.listdir(assets_dir) == 0:
        print("WARNING: Assets directory is empty")

    print(f"Using notebook: {get_jupyter_notebook_path()} for submission...")

    # Remove existing files from submission directoru
    if os.path.exists(SUBMISSION_DIR):
        print("Removing existing files from submission directory...")
        shutil.rmtree(SUBMISSION_DIR)
    os.mkdir(SUBMISSION_DIR)

    # Clean sensitive stuff from notebook
    cleaned_notebook_path = os.path.join(SUBMISSION_DIR, "original_notebook.ipynb")
    if notebook_name is None:
        notebook_name = get_notebook_path()
    clean_notebook(notebook_name, cleaned_notebook_path)

    # Breaks the notebook into {install, train, predict}.ipynb
    split_notebook(cleaned_notebook_path, SUBMISSION_DIR)
    # Write aicrowd.json
    write_aicrowd_config(SUBMISSION_DIR)
    # Copy the original notebook
    # bundle_notebook(submission_zip_path, notebook_name)
    # Copy assets
    shutil.copytree(assets_dir, os.path.join(SUBMISSION_DIR, assets_dir))
    # Zip everything
    shutil.make_archive(submission_zip_path.replace(".zip", ""), "zip", SUBMISSION_DIR)


def create_submission(
    challenge: str,
    description: str,
    assets_dir: str,
    submission_zip_path: str = "submission.zip",
    notebook_name: str = None,
    no_verify: bool = False,
    dry_run: bool = False,
):
    bundle_submission(assets_dir, submission_zip_path, notebook_name)
    if not no_verify:
        verify_submission()
    if not dry_run:
        submit_to_aicrowd(
            challenge=challenge,
            file_path=submission_zip_path,
            description=description,
            print_links=True,
        )
