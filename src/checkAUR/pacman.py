"""Module responsible for getting information from pacman
"""

import subprocess
from typing import Optional, Final
import re

from checkAUR.common.package import Package


def extract_local_packages() -> set[Package]:
    """use pacman query to get locally installed packages (outside of repos)

    Raises:
        UnicodeError: if stdout from pacman could not be read as string

    Returns:
        set[Package]: packages installed locally
    """
    query_result = subprocess.run(
        "pacman -Qm",
        shell=True,
        capture_output=True,
        check=True
    )
    try:
        decoded_string = query_result.stdout.decode(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise UnicodeError from exc
    return set(package for package_string in decoded_string.split(sep="\n") \
    if (package := _extract_package_name(package_string)) is not None)


_PACKAGE_NAME_PATTERN: Final[re.Pattern] = re.compile(r"(.+)( )(.+)(-\d+)")


def _extract_package_name(checked_name: str) -> Optional[Package]:
    found: Optional[re.Match] = re.search(_PACKAGE_NAME_PATTERN, checked_name)
    if found is None:
        return None
    extracted_name: str = found[1]
    if extracted_name.endswith("-debug"):
        extracted_name = extracted_name[:-6]
    return Package(name=extracted_name, version=found[3])
