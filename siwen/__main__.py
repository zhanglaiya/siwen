import argparse
from . import __version__


def get_version():
    return __version__


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', dest='version')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.version:
        print(get_version())


if __name__ == '__main__':
    main()
