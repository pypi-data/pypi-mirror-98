"""
Submission subcommand
"""
import os
import sys

import click

from aicrowd.contexts import (
    pass_config,
    ConfigContext,
    pass_challenge,
    ChallengeContext,
)
from aicrowd.errors import UNKNOWN_ERROR, INVALID_FILE
from aicrowd.utils import AliasedGroup


@click.group(name="submission", cls=AliasedGroup)
def submission_command():
    """
    Create and view submissions
    """


@click.command(name="create")
@click.option(
    "-c",
    "--challenge",
    type=str,
    help="Specify challenge explicitly",
)
@click.option(
    "-f",
    "--file",
    "file_path",
    type=click.Path(),
    default="",
    help="The file to submit",
)
@click.option(
    "-d",
    "--description",
    type=str,
    help="Description",
    default="",
)
@click.option("--jupyter", is_flag=True, help="Bundle jupyter notebook")
@pass_challenge
@pass_config
def create_subcommand(
    config_ctx: ConfigContext,
    challenge_ctx: ChallengeContext,
    challenge: str,
    file_path: str,
    description: str,
    jupyter: bool,
):
    """
    Create a submission on AIcrowd
    """
    if not jupyter and not os.path.exists(file_path):
        click.echo(
            click.style(f"Submission file {file_path} does not exist", fg="red"),
            err=True,
        )
        sys.exit(INVALID_FILE)

    from aicrowd.submission import create
    from aicrowd.submission.exceptions import SubmissionException

    try:
        print(
            create(
                challenge,
                file_path,
                description,
                True,
                config_ctx,
                challenge_ctx,
                jupyter=jupyter,
            )
        )
    except SubmissionException as e:
        message = e.message
        # separated to avoid cases where message is none
        if not message:
            message = (
                "An unknown error occured. Please set verbosity to check full logs."
            )

        click.echo(click.style(message, fg="red"), err=True)
        if e.fix:
            click.echo(click.style(e.fix, fg="yellow"))

        sys.exit(e.exit_code)


@click.command(name="save-assets")
@click.option(
    "-c",
    "--challenge",
    type=str,
    help="Specify challenge explicitly",
)
def save_assets_subcommand(challenge: str):
    from aicrowd.submission.copy_assets import copy_assets

    copy_assets(challenge, colab_to_drive=True)


@click.command(name="load-assets")
@click.option(
    "-c",
    "--challenge",
    type=str,
    help="Specify challenge explicitly",
)
def load_assets_subcommand(challenge: str):
    from aicrowd.submission.copy_assets import copy_assets

    copy_assets(challenge, colab_to_drive=False)


submission_command.add_command(create_subcommand)
submission_command.add_command(save_assets_subcommand)
submission_command.add_command(load_assets_subcommand)
