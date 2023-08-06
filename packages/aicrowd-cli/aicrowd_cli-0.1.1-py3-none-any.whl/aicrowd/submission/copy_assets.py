"""
Subcommand to copy the assets to user's google drive
"""

import logging
import os

import click

from aicrowd.submission.helpers import delete_and_copy_dir
from aicrowd.utils.jupyter import (
    is_google_colab_env,
    mount_google_drive,
    get_assets_dir,
)


def copy_assets(
    challenge: str,
    colab_to_drive: bool = True,
):
    """
    Copy the assets from local FS to google drive and vice-versa. These assets will later be used
    in the inference notebooks.

    Args:
        challenge: Challenge identifier
        colab_to_drive: Direction of the copy
    """
    log = logging.getLogger()
    if not is_google_colab_env():
        log.debug("Checking for google colab env")
        click.echo(
            click.style("This command should only be run on Google Colab Notebooks")
        )
        raise RuntimeError("Not running on google colab")

    assets_dir = get_assets_dir()
    if colab_to_drive and not os.path.exists(assets_dir):
        raise FileNotFoundError(f"ASSETS_DIR: {assets_dir} does not exist")

    log.debug("Mounting google drive")
    mount_path = mount_google_drive(
        mount_reason="Google drive is needed to store your assets"
    )
    log.debug("Copying assets to google drive")
    drive_path = os.path.join(mount_path, "My Drive/aicrowd/challenges", challenge)
    if colab_to_drive:
        delete_and_copy_dir(assets_dir, drive_path)
    else:
        delete_and_copy_dir(drive_path, assets_dir)
    log.debug("Copied assets to google drive")
