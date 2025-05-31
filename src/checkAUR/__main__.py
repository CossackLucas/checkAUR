"""Main for checkAUR
"""

from checkAUR.check_user import check_if_root


def main():
    if check_if_root():
        return
    print("Not root")


if __name__ == "__main__":
    main()
