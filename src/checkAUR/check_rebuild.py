"""Module responsible for using checkrebuild
"""
import subprocess
import re

from checkAUR.common.custom_logging import logger
from checkAUR.common.exceptions import ProgramNotInstalledError


def check_rebuild() -> tuple[str,...]:
    """check AUR packages requiring updates

    Returns:
        tuple[str,...]: tuple of packages requiring updates
    Raises:
        ProgramNotInstalledError: if checkrebuild is not available
        UnicodeError: if it's not possible to convert stdout to string
    """
    try:
        result: subprocess.CompletedProcess = subprocess.run("checkrebuild",
            shell=True, capture_output=True, check=True
        )
    except subprocess.CalledProcessError as exc:
        message = "checkrebuild not available"
        print(message)
        logger.error(message)
        raise ProgramNotInstalledError("rebuild-detector") from exc
    stdout: bytes = result.stdout
    try:
        return extract_packages(stdout)
    except UnicodeError as exc:
        raise UnicodeError from exc


def extract_packages(stdout: bytes) -> tuple[str,...]:
    """extract package data from stdout

    Args:
        stdout (bytes): stdout from checkrebuild

    Raises:
        UnicodeError: if it's not possible to convert stdout to string

    Returns:
        tuple[str,...]: tuple of packages requiring updates
    """
    try:
        conversion: str = stdout.decode(encoding="utf-8", errors="strict")
    except UnicodeError as exc:
        raise UnicodeError("stdout could not be converted to string") from exc
    search_result: list[re.Match] = re.findall(r"(foreign)\t(.+)\n", conversion)
    return tuple(element[1] for element in search_result)



def print_invalid_packages(invalid_packages: tuple[str,...]) -> None:
    """print list of all packages, marked as invalid by checkrbuild

    Args:
        invalid_packages (tuple[str,...]): tuple of invalid packages
    """
    logger.debug("Printing package list")
    print("AUR packages with issues:")
    for package in invalid_packages:
        print(f"\t{package}")


if __name__ == "__main__":
    check_rebuild()
