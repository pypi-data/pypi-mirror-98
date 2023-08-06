"""
For handling logins
"""

import sys
import logging

import click

from aicrowd.contexts import pass_config, ConfigContext


@click.command(name="login")
@click.option("--api-key", type=str, help="API Key from AIcrowd website")
@pass_config
def login_command(config_context: ConfigContext, api_key: str):
    """
    Log in using AIcrowd API Key
    """
    from aicrowd.auth import login
    from aicrowd.auth.exceptions import LoginException

    log = logging.getLogger()

    if api_key is None:
        log.info("API Key not provided in parameters, prompting")

        click.launch("https://www.aicrowd.com/participants/me")
        click.echo("Please copy paste the API Key")
        api_key = click.prompt("API Key")

    try:
        login(api_key, config_context)
    except LoginException as e:
        click.echo(click.style(e.message, fg="red"))
        if e.fix:
            click.echo(click.style(e.fix, fg="yellow"))
        sys.exit(e.exit_code)
