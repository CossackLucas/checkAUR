"""Module printing result of the work
"""

from typing import Optional

from checkAUR.common.package import Package, find_package
from checkAUR.common.data_classes import TuplePackages

type PackageData = tuple[Package,...]


def print_differences_packages(pulled_packages: PackageData,
    invalid_packages: tuple[str,...]
) -> None:
    """print information on packages waiting for update and packages marked by checkrebuild

    Args:
        pulled_packages (PackageData): list of packages updated by Git
        invalid_packages (tuple[str,...]): list of packages marked by checkrebuild
    """
    if len(invalid_packages) == 0:
        return

    pulled_names: set[str] = set(package.name for package in pulled_packages)
    result: tuple[str,...] = compare_invalid_packages(pulled_names, invalid_packages)
    if len(result) == 0:
        print("All packages marked by checkrebuild are among the updated")
        return

    print("Invalid packages, marked by checkrebuild and without an update:")
    for data in result:
        print(f"\t{data}")


def compare_invalid_packages(pulled_packages: set[str],
    invalid_packages: tuple[str,...]
) -> tuple[str,...]:
    """compare invalid packages with pulled packages

    Args:
        pulled_packages (set[str): updated packages
        invalid_packages (tuple[str,...]): packages marked by checkrebuild

    Returns:
        tuple[str,...]: tuple of packages among the invalid packages, but not updated by Git
    """
    return tuple(package for package in invalid_packages if package not in pulled_packages)


def compare_packages(aur_packages: PackageData, pacman_packages: PackageData) -> PackageData:
    """compare data from pacman and data found in AUR directory

    Args:
        aur_packages (PackageData): tuple of packages found in AUR directory
        pacman_packages (PackageData): tuple of packages found in pacman

    Returns:
        PackageData: AUR packages ready for an update
    """
    result: list[Package] = []
    for package in aur_packages:
        check: Optional[Package] = find_package(package.name, pacman_packages)
        if check is None:
            continue

        if package > check:
            result.append(package)
    return tuple(result)


def print_pulled_packages(pulled_packages: PackageData) -> None:
    """print the tuple of pulled packages

    Args:
        pulled_packages (PackageData): tuple of pulled packages
    """
    count_pulled_packages = len(pulled_packages)
    print(f"{count_pulled_packages} packages were pulled.")
    if count_pulled_packages == 0:
        return

    for package in pulled_packages:
        print(f"\t{package}")


def print_awaiting_packages(compared_packages: PackageData, pacman_packages: PackageData) -> None:
    """print the list of packages awaiting an update

    Args:
        compared_packages (PackageData): tuple of all awaiting packages
        pacman_packages (PackageData): tuple of all manually installed packages
    """
    if len(compared_packages) == 0:
        print("No updates detected")
        return
    print("Following AUR packages await an update:")
    for package in compared_packages:
        original_package = find_package(package.name, pacman_packages)
        print(f"\t{original_package} to {package.version}")


def show_results(operation_results: TuplePackages) -> bool:
    """show the user the results of all the operations

    Args:
        operation_results (TuplePackages): NamedTuple containing all package tuples
    
    Returns:
        bool: True if there packages to build in AUR directiory
    """
    # Todo: there should be sth for AUR package groups!
    print_pulled_packages(operation_results.pulled_packages)
    compared_packages = compare_packages(
        operation_results.aur_packages,
        operation_results.pacman_packages
    )
    print_differences_packages(compared_packages, operation_results.invalid_packages)
    print_awaiting_packages(compared_packages, operation_results.pacman_packages)

    return bool(len(compared_packages) != 0 or len(operation_results.invalid_packages) != 0)
