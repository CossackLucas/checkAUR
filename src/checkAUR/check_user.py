"""Checking user id
"""

import os

from checkAUR.common.custom_logging import logger


def check_if_root() -> bool:
    """check if user executing the program is the root

    Returns:
        bool: if it's root then True
    """
    if os.getuid() == 0:
        message = "Should not be run as root!"
        print(message)
        logger.critical(message)
        return True
    return False
