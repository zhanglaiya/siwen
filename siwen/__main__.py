import argparse
import optparse
from . import version


def get_version():
    return version


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', dest='version', action='store_true', help='ss')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.version:
        print(get_version())


if __name__ == '__main__':
    main()
