"""
Dataset subcommand
"""

import sys
from typing import List

import click

from aicrowd.contexts import (
    pass_config,
    ConfigContext,
    pass_challenge,
    ChallengeContext,
)
from aicrowd.utils import AliasedGroup


@click.group(name="dataset", cls=AliasedGroup)
def dataset_command():
    """
    View and download datasets
    """


@click.command(name="list")
@click.option("-c", "--challenge", type=str, help="Specify challenge explicitly")
@pass_challenge
@pass_config
def list_subcommand(
    config_ctx: ConfigContext, challenge_ctx: ChallengeContext, challenge: str
):
    """
    List the dataset files
    """
    from aicrowd.dataset import list_
    from aicrowd.dataset.exceptions import DatasetException

    try:
        list_(challenge, False, config_ctx, challenge_ctx)
    except DatasetException as e:
        click.echo(click.style(e.message, fg="red"))
        if e.fix:
            click.echo(click.style(e.fix, fg="yellow"))
        sys.exit(e.exit_code)


@click.command(name="download")
@click.option("-c", "--challenge", type=str, help="Specify challenge explicitly")
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(exists=True),
    help="Specify dataset download directory",
    default=".",
)
@click.option("-j", "--jobs", type=int, help="Number of files to download in parallel")
@click.argument("datasets", nargs=-1, type=str)
@pass_challenge
@pass_config
def download_subcommand(
    config_ctx: ConfigContext,
    challenge_ctx: ChallengeContext,
    challenge: str,
    output_dir: str,
    jobs: int,
    datasets: List[str],
):
    """
    Download dataset files
    """
    from aicrowd.dataset import download
    from aicrowd.dataset.exceptions import DatasetException

    try:
        download(challenge, output_dir, jobs, datasets, config_ctx, challenge_ctx)
    except DatasetException as e:
        click.echo(click.style(e.message, fg="red"))
        if e.fix:
            click.echo(click.style(e.fix, fg="yellow"))
        sys.exit(e.exit_code)


dataset_command.add_command(list_subcommand)
dataset_command.add_command(download_subcommand)
