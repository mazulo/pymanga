import argparse
import urllib

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(
        prog='PyManga',
        description='An easily way to download your favorite mangas'
    )
    parser.add_argument(
        '-a', '--anime',
        type=str, help="Type the anime's name"
    )
    parser.add_argument(
        '-c', '--chapter',
        type=str, help="Type the chapter you wish"
    )

    args = parser.parse_args()

if __name__ == '__main__':
    main()

