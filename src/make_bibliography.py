import argparse
import os

import bibtexparser
from mako.template import Template


TEMPLATE_DIR = r'../templates'
OUTPUT_DIR = r'../output'
TEMPLATES = {
    'graduttaja': 'graduttaja.mako',
}


def make_bibliography(
        database,
        output,
        style,
):
    os.chdir(TEMPLATE_DIR)
    items = ['a', 3, 'c']
    template = Template(filename=TEMPLATES[style])

    os.chdir(OUTPUT_DIR)
    with open(output, 'w') as fopen:
        print(template.render(items=items), file=fopen)


def main():
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
        help=f"Style to use {tuple(TEMPLATES)}",
    )
    args = argparser.parse_args()
    make_bibliography(
        database=args.db,
        output=args.output,
        style=args.style,
    )


if __name__ == '__main__':
    make_bibliography(
        database=None,
        output=r'testi.txt',
        style='graduttaja',
    )
    # main()
