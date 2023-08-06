"""
Subcommand to copy the assets to user's google drive
"""

import logging
import os
import shutil

import click

from aicrowd.submission.helpers import mount_google_drive
from aicrowd.utils.jupyter import is_google_colab_env


def load_assets(
    challenge: str,
    assets_dir: str,
):
    """
    Copy the assets from local FS to google drive. These assets will later be used
    in the inference notebooks.

    Args:
        challenge: Challenge identifier
        assets_dir: Path to the directory containing assets

    Raises:
        RuntimeError: If the command is triggered outside google colab notebook
    """
    log = logging.getLogger()
    if not is_google_colab_env():
        log.debug("Checking for google colab env")
        click.echo(
            click.style("This command should only be run on Google Colab Notebooks")
        )
        raise RuntimeError("Not running on google colab")

    log.debug("Mounting google drive")
    mount_path = mount_google_drive(
        mount_reason="Google drive is needed to store your assets"
    )
    log.debug("Copying assets to google drive")
    shutil.copytree(assets_dir, os.path.join(mount_path, "aicrowd", challenge))
    log.debug("Copied assets to google drive")
