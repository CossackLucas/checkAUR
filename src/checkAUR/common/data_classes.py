"""Module for common data classes
"""

from typing import NamedTuple
from pathlib import Path

from checkAUR.common.package import Package


class EnvVariables(NamedTuple):
    """aggregator class for used environment variables
    """
    aur_path: Path


class TuplePackages(NamedTuple):
    aur_packages: tuple[Package,...]
    pacman_packages: tuple[Package,...]
    pulled_packages: tuple[Package,...]
    invalid_packages: tuple[str,...]
