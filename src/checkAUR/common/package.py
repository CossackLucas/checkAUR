"""Module for Package class
"""

from typing import NamedTuple


class Package(NamedTuple):
    """Named tuple containing package name and its version

    Attributes:
        name (str): name of the package (can contain suffixes like -bin, -git etc.)
        version (str): description of the version
    """
    name: str
    version: str

    def __eq__(self, other_package) -> bool:
        if self.name != other_package.name:
            return False
        return bool(self.version == other_package.version)

    def __ne__(self, other_package) -> bool:
        if self.name != other_package.name:
            return False
        return bool(self.version != other_package.version)
