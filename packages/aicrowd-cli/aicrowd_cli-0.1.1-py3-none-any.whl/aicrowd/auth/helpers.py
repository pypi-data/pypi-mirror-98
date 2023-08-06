"""
Auth related tasks
"""

import logging
import requests

from aicrowd.constants import RAILS_API_ENDPOINT


def verify_api_key(api_key: str) -> bool:
    """
    Verifies if the API Key is valid or not

    Args:
        api_key: AIcrowd API Key

    Returns:
        True if API Key valid, False otherwise
    """
    log = logging.getLogger()

    r = requests.get(
        f"{RAILS_API_ENDPOINT}/api_user",
        headers={"Authorization": f"Token {api_key}"},
    )

    if not r.ok:
        log.error(
            "Error in verifying API Key.\nReason: %s, Message: %s", r.reason, r.text
        )

    return r.ok
