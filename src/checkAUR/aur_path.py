"""Modul responsible for setting the localization
"""

import logging
from pathlib import Path
from dotenv import find_dotenv, set_key

def set_aur_localization(aur_path: Path) -> bool:
    """Set localization of the private AUR folders

    Args:
        aur_path (Path): path to the AUR folder
    
    Returns:
        bool: True if successful, False if not
    """
    if not isinstance(aur_path, Path):
        message = "The given path for AUR was not proper Path!"
        logging.error(message)
        print(message)
        return False
    if not aur_path.is_absolute():
        message = "The path has to be absolute!"
        logging.error(message)
        print(message)
        return False
    if not aur_path.is_dir():
        message = "The path does not lead to a folder!"
        logging.error(message)
        print(message)
        return False

    try:
        env_path = find_dotenv(raise_error_if_not_found=True)
    except IOError:
        message = ".env file not found!"
        logging.error(message)
        print(message)
        return False

    set_key(env_path, "aur_path", aur_path.as_posix())

    return True
