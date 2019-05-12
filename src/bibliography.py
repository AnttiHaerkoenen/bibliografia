from collections import OrderedDict
from operator import attrgetter
from typing import Sequence

import bibtexparser.customization as bibcust


def handle_authors(
        entry: dict,
) -> dict:
    """
    Sets 'author' to:
        1) list of dicts of lists
        (each author passed through bibtexparser.customization.splitname)
        2) None, if 'author' not in entry

    Example:
        entry['author'] = [
                {
                    'first': ['J.', 'L.'],
                    'last': 'Bredas',
                    'von': '',
                    'jr': '',
                },
                {
                    'first': ['Georg', 'Henrik'],
                    'last': 'Wright',
                    'von': 'von',
                    'jr': '',
                },
            ]
    :param seps: Separators to use, default ' and ',
    :param entry: entry-dict
    :return: entry-dict with formatted author
    """
    if 'author' in entry:
        authors = entry['author'].split(' and ')
        authors_ = []
        for au in authors:
            au_dict = bibcust.splitname(au)
            au_dict_new = {k: (v[0] if v else '') for k, v in au_dict.items()}
            au_dict_new['first'] = au_dict['first']
            authors_.append(au_dict_new)
        entry['author'] = authors_
    else:
        entry['author'] = None
    return entry


def handle_date(entry: dict) -> dict:
    """
    Sets 'date' to:
        1) list of year, month and day
        2) None if 'date' not in entry
    Sets 'year' to:
        1) date[0]
        2) None if 'date' not in entry
    :param entry:
    :return:
    """
    if 'date' in entry:
        date = entry['date'].split('-')
        entry['date'] = date
        entry['year'] = date[0]
    else:
        entry['date'] = None
        entry['year'] = None
    return entry


def handle_pages(
        entry: dict,
        seps: Sequence = ('--', '‐', '‑', '–', '—', '-', '−'),
) -> dict:
    """
    Sets 'pages' to:
        1) list of page numbers
        2) None if 'date' not in entry
    :param seps: Sequence of separators to use (in order)
    :param entry: dict
    :return: entry dict
    """
    if 'pages' in entry:
        pages = entry['pages']
        for sep in seps:
            pages = pages.replace(sep, '*')
        entry['pages'] = pages.split('*')
    else:
        entry['pages'] = None
    return entry


def handle_entry(entry: dict) -> dict:
    """
    Reforms entry using functions from bibtexparser.customization
    and handle_authors
    :param entry: parsed bibtex-record as a dict
    :return: standardised record as a dict
    """
    entry = bibcust.convert_to_unicode(entry)
    entry = handle_authors(entry)
    entry = handle_pages(entry)
    entry = handle_date(entry)
    entry = bibcust.type(entry)
    entry = bibcust.doi(entry)
    for field in 'number volume doi journaltitle'.split():
        if field not in entry:
            entry[field] = None
    return entry


class Bibliography:
    def __init__(self, entries: dict):
        self.entries_dict: OrderedDict = OrderedDict(
            {k: handle_entry(v) for k, v in entries.items()}
        )
        self._set_letters()

    @property
    def entries(self) -> list:
        return [e for e in self.entries_dict.values()]

    def _set_letters(self):
        pass


if __name__ == '__main__':
    n = "Orti, E. and Bredas, J. L. and Clarisse, C.".split(' and ')
    print(bibcust.splitname("von Wright, Georg Henrik"))
