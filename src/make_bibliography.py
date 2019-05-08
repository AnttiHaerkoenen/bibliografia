import argparse

import attr
import bibtexparser


def make_bibliography(
        database,
        target,
        style,
):
    pass


if __name__ == '__main__':
    argparser = argparse.ArgumentParser("Create text bibliography from bibtex")
    argparser.add_argument(
        'db',
        target='databases',
        help="Input bibtex-file",
    )
    argparser.add_argument(
        '--output',
        target='output',
        help="Output .txt-file",
    )
    argparser.add_argument(
        '--style',
        target='style',
        help=f"Style to use {tuple(styles.keys())}",
    )
    args = argparser.parse_args()
    make_bibliography(
        database=args.db,
        target=args.target,
        style=args.style
    )
