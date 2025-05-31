"""Module printing result of the work
"""


type PackageData = tuple[str,...]


def compare_packages(pulled_packages: PackageData, invalid_packages: PackageData) -> None:
    count_pulled_packages = len(pulled_packages)
    print(f"{count_pulled_packages} packages were pulled.")
    if count_pulled_packages != 0:
        for package in pulled_packages:
            print(package)

    if len(invalid_packages) == 0:
        return
    

    result = compare_invalid_packages(pulled_packages, invalid_packages)
    if len(result) == 0:
        print("All packages marked by checkrebuild are among updated")
        return

    print("Invalid packages, marked by checkruild and not updated:")
    for package in result:
        print(package)


def compare_invalid_packages(pulled_packages: PackageData, invalid_packages: PackageData) -> PackageData:
    result: list[str] = []
    for package in invalid_packages:
        if package not in pulled_packages:
            result.append(package)

    return tuple(result)
