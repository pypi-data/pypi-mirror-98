"""
Challenge subcommand
"""

import sys

import click

from aicrowd.contexts import pass_config, ConfigContext
from aicrowd.utils import AliasedGroup


@click.group(name="challenge", cls=AliasedGroup)
def challenge_command():
    """
    Setup a challenge
    """


@click.command(name="init")
@click.argument("challenge", type=str)
@click.option(
    "-d",
    "--base-dir",
    type=click.Path(exists=True),
    help="Base directory for storing the challenge",
)
@click.option(
    "--mkdir",
    is_flag=True,
    help="Create a new directory for challenge inside current directory",
)
@pass_config
def init_subcommand(
    config_ctx: ConfigContext, challenge: str, base_dir: str, mkdir: bool
):
    """
    Setups basic challenge files
    """
    from aicrowd.challenge import init
    from aicrowd.challenge.exceptions import ChallengeException

    try:
        init(challenge, base_dir, mkdir, config_ctx)
    except ChallengeException as e:
        click.echo(click.style(e.message, fg="red"))
        if e.fix:
            click.echo(click.style(e.fix, fg="yellow"))
        sys.exit(e.exit_code)


challenge_command.add_command(init_subcommand)
