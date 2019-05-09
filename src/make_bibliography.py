import argparse
import os

import bibtexparser
from mako.template import Template

from src.bibliography import Bibliography


TEMPLATE_DIR = r'../templates'
TEMPLATES = {
    'graduttaja': 'graduttaja.mako',
    # 'terra': 'terra.mako',
}


def make_bibliography(
        database,
        output,
        style,
):
    with open(database) as fopen:
        database = bibtexparser.load(fopen)
    articles = list(filter(lambda e: e['ENTRYTYPE'] in 'article incollection misc book'.split(), database.entries))
    entries = Bibliography(entries)
    os.chdir(TEMPLATE_DIR)
    template = Template(filename=TEMPLATES[style])

    with open(output, 'w') as fopen:
        print(template.render(entries=entries), file=fopen)


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
        database=r'../data/bib.bib',
        output=r'../output/testi.html',
        style='graduttaja',
    )
    # main()
