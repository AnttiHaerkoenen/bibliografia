import argparse
import os

import bibtexparser
from mako.template import Template
from mako.lookup import TemplateLookup

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
    parser = bibtexparser.bparser.BibTexParser()
    parser.ignore_nonstandard_types = False
    parser.homogenize_fields = True
    parser.add_missing_from_crossref = True
    with open(database) as fopen:
        database = bibtexparser.load(fopen, parser=parser)
    articles = list(filter(lambda e: e['ENTRYTYPE'] in 'article incollection misc book'.split(), database.entries))
    entries = Bibliography(database.entries_dict)
    os.chdir(TEMPLATE_DIR)
    look_up = TemplateLookup(directories=TEMPLATE_DIR, input_encoding='utf-8')
    template = Template(filename=TEMPLATES[style], lookup=look_up)

    with open(output, 'w') as fopen:
        print(template.render(entries=entries.entries), file=fopen)


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
        database=r'../data/refworks.bib',
        output=r'../output/testi.html',
        style='graduttaja',
    )
    # main()
