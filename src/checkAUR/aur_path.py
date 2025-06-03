"""Modul responsible for setting the localization
"""

import logging
import os
from pathlib import Path

import dotenv
from checkAUR.common.data_classes import EnvVariables

def set_aur_path(aur_path: Path) -> bool:
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

    setting_env_variable(aur_path)
    return True


def setting_env_variable(aur_path: Path):
    """set environment variable for local AUR repo

    Args:
        aur_path (Path): path to the AUR folder

    Raises:
        EnvironmentError: if neither .env file nor environment variable could be find
    """
    # Todo: probably should check .env first and then add env variable anyway
    env_var = os.environ.get("aur_path")
    if env_var is not None:
        os.environ["aur_path"] = aur_path.as_posix()
        return
    try:
        env_path = dotenv.find_dotenv(raise_error_if_not_found=True)
    except IOError as exc:
        message = ".env file not found!"
        logging.error(message)
        print(message)
        raise EnvironmentError("Environament variable could not be set") from exc

    dotenv.set_key(env_path, "aur_path", aur_path.as_posix())


def load_env() -> EnvVariables:
    """load required environment variables

    Raises:
        EnvironmentError: if it's not possible to find required variables

    Returns:
        EnvVariables: NamedTuple of environmental variables
    """
    env_exception = None
    try:
        env_file = dotenv.find_dotenv(raise_error_if_not_found=True)
    except IOError as exc:
        env_exception = exc
    else:
        dotenv.load_dotenv(env_file)

    env_var = os.environ.get("aur_path")
    if env_var is None:
        message = ".env file not found!"
        logging.critical(message)
        print(message)
        raise EnvironmentError("Environament variable could not be extracted") from env_exception

    return EnvVariables(aur_path=Path(env_var))
