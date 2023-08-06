"""Console script for justice."""
import argparse
import pprint
import sys

from justice.justice import Justice


def main():
    """Console script for justice."""
    pp = pprint.PrettyPrinter(indent=4)

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--get', type=str, nargs='*')
    parser.add_argument('-s', '--search', type=str, nargs='+')
    args = parser.parse_args()

    if args.get:
        for subject in args.get:
            pp.pprint(Justice.get_detail(subject_id=subject))
    elif args.search:
        pp.pprint(Justice.search(string=' '.join(args.search)))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
