"""Module for Package class
"""

from typing import Self, Optional, Final
from dataclasses import dataclass
import subprocess
import re
from pathlib import Path
import os


class ComparisonException(Exception):
    """Custom exception for comparing wrong packages
    """
    def __init__(self, *args):
        super().__init__("Comparisons are only possible with the same package names", args)


@dataclass(frozen=True, eq=True, slots=True)
class Package:
    """Dataclass containing package's name and its version.
    Equality can be done on any packages, but comparisons only work on versions, names have to be the same!

    Attributes:
        name (str): name of the package (can contain suffixes like -bin, -git etc.)
        version (str): description of the version
    """
    name: str
    version: str

    def __post_init__(self):
        # Hack to go over inconsitencies in PKGBUILDs and pacman
        object.__setattr__(self, "version", self.version.replace("-", "_"))

    def __str__(self):
        return self.name + " " + self.version

    def _compare_version(self, other_package: Self, operation: str) -> bool:
        assert isinstance(operation, str)
        if self.name != other_package.name or not isinstance(other_package, Package):
            raise ComparisonException
        vercmp_result = subprocess.run(f"vercmp {self.version} {other_package.version}",
        capture_output=True, check=True, shell=True)
        result = int(vercmp_result.stdout.decode(encoding="utf-8"))
        match operation:
            case ">" if result > 0:
                pass
            case ">=" if result >= 0:
                pass
            case "<" if result < 0:
                pass
            case "<=" if result <= 0:
                pass
            case _:
                return False
        return True

    def __lt__(self, other_package: Self) -> bool:
        return self._compare_version(other_package, "<")

    def __gt__(self, other_package: Self) -> bool:
        return self._compare_version(other_package, ">")

    def __le__(self, other_package: Self) -> bool:
        return self._compare_version(other_package, "<=")

    def __ge__(self, other_package: Self) -> bool:
        return self._compare_version(other_package, ">=")


def find_package(package_name:str, packages: set[Package]) -> Optional[Package]:
    """find by name package in the collection

    Args:
        package_name (str): name of the looked for package
        packages (set[Package]): collection of the packages

    Returns:
        Optional[Package]: if match not found, return None
    """
    for package in packages:
        if package.name == package_name:
            return package
    return None


VERSION_PATTERN: Final[re.Pattern] = re.compile("pkgver=(.*)\n")
EPOCH_PATTERN: Final[re.Pattern] = re.compile("epoch=(.*)\n")


def read_version_pkgbuild(repo_path: Path) -> str:
    """read pkgbuild in the given directory and return read version of the package

    Args:
        repo_path (Path): path to AUR repo

    Returns:
        str: string with package version
    """
    epoch: Optional[str] = None
    result: Optional[str] = None
    with open(repo_path / "PKGBUILD", "r", buffering=1, encoding="utf-8") as file:
        for line in file:
            if epoch is not None and result is not None:
                break

            search_epoch = re.search(EPOCH_PATTERN, line)
            if search_epoch is not None and epoch is None:
                epoch = search_epoch[1]

            search_result = re.search(VERSION_PATTERN, line)
            if search_result is not None and result is None:
                result = search_result[1]

    epoch = "" if epoch is None else epoch + ":"

    if result is not None:
        return epoch + result

    return "NDA"


def read_pkgbuild(repo_path: Path) -> Package:
    """read pkgbuild in the given directory and return package information

    Args:
        repo_path (Path): path to AUR repo

    Returns:
        Package: object describing the entire package
    """
    version = read_version_pkgbuild(repo_path)
    # Todo: should name be taken from PKGBUILD?
    return Package(repo_path.stem, version)


def read_enitre_repo_pkgbuild(aur_path: Path) -> set[Package]:
    """read all packages from folder using PKGBUILD files as base

    Args:
        aur_path (Path): path to AUR repos folder

    Returns:
        set[Package]: packages found
    """
    folder_list: list[str] = os.listdir(aur_path)
    repo_tuple: tuple[Path,...] = tuple((aur_path / folder) for folder in folder_list)
    return set(read_pkgbuild(repo) for repo in repo_tuple)
