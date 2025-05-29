"""Main for checkAUR
"""
import os


def main():
    if os.getuid() == 0:
        return
    print("Not root")


if __name__ == "__main__":
    main()
