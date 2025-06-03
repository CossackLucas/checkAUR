"""Module responsible for getting information from pacman
"""

import subprocess
from typing import Optional
import re

from checkAUR.common.package import Package


def extract_manual_packages() -> set[Package]:
    query_result = subprocess.run("pacman -Qm", shell=True, capture_output=True, check=True)
    return _sort_pacman_data(query_result.stdout)


def _sort_pacman_data(stdout: bytes) -> set[Package]:
    try:
        decoded_string = stdout.decode(encoding="utf-8")
    except UnicodeEncodeError:
        pass
    return set(package for package_string in decoded_string.split(sep="\n") if (package := _extract_package_name(package_string)) is not None)


_package_name_pattern = re.compile(r"(.+)( )(.+)(-\d+)")


def _extract_package_name(checked_name: str) -> Optional[Package]:
    found = re.search(_package_name_pattern, checked_name)
    if found is None:
        return None
    extracted_name = found[1]
    if extracted_name.endswith("-debug"):
        extracted_name = extracted_name[:-6]
    return Package(name=extracted_name, version=found[3])


if __name__ == "__main__":
    print(extract_manual_packages())
