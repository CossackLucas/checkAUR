"""Checking user id
"""

import os
import logging


def check_if_root() -> bool:
    """check if user executing the program is the root

    Returns:
        bool: if it's root then True
    """
    if os.getuid() == 0:
        message = "Should not be run as root!"
        print(message)
        logging.critical(message)
        return True
    return False
