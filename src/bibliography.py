from collections import OrderedDict
from collections.abc import Sequence

import bibtexparser.customization as bib_custom


def handle_authors(
        entry: dict,
) -> dict:
    """
    Sets 'author' to:
        1) list of dicts of lists
        (each author passed through bibtexparser.customization.splitname)
        2) None, if 'author' not in item_

    Example:
        item_['author'] = [
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
    :param entry: item_-dict
    :return: item_-dict with formatted author
    """
    if 'author' in entry:
        authors = entry['author'].split(' and ')
        authors_ = []
        for au in authors:
            au_dict = bib_custom.splitname(au)
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
        2) None if 'date' not in item_
    Sets 'year' to:
        1) date[0]
        2) None if 'date' not in item_
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
        2) None if 'date' not in item_
    :param seps: Sequence of separators to use (in order)
    :param entry: dict
    :return: item_ dict
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
    Reforms item_ using functions from bibtexparser.customization
    and handle_authors
    :param entry: parsed bibtex-record as a dict
    :return: standardised record as a dict
    """
    entry = bib_custom.convert_to_unicode(entry)
    entry = handle_authors(entry)
    entry = handle_pages(entry)
    entry = handle_date(entry)
    entry = bib_custom.type(entry)
    entry = bib_custom.doi(entry)
    for field in 'number volume doi journaltitle'.split():
        if field not in entry:
            entry[field] = None
    return entry


class Bibliography:
    def __init__(self, entries: dict):
        self.entries_dict: OrderedDict = OrderedDict(
            {k: handle_entry(v) for k, v in entries.items()}
        )
        self._handle_duplicates()

    @property
    def entries(self) -> list:
        return [e for e in self.entries_dict.values()]

    @property
    def authors_years_dict(self) -> dict:
        return {k: self.author_year_getter(entry) for k, entry in self.entries_dict.items()}

    @property
    def authors_years(self) -> list:
        return [entry for entry in self.authors_years_dict.values()]

    @property
    def unique_authors_years(self) -> dict:
        unique_authors_years = {}
        for k, v in self.authors_years_dict.items():
            if v in unique_authors_years:
                unique_authors_years[v].append(k)
            else:
                unique_authors_years[v] = [k]
        return unique_authors_years

    def sort(self):
        self.entries_dict = OrderedDict(sorted(
            self.entries_dict.items(),
            key=lambda key_val: self.author_year_getter(key_val[1]),
        ))

    @staticmethod
    def author_year_getter(entry):
        author = entry['author']
        if not author:
            author = tuple()
        elif len(author) <= 3:
            author = tuple([au['last'] for au in author])
        else:
            author = author[0]['last'], 'et al.'
        return author, entry['year']

    def _handle_duplicates(self):
        self.sort()

        # delete duplicates
        duplicates = []
        last_entry = None
        for k, entry in self.entries_dict.items():
            if entry == last_entry:
                duplicates.append(k)
            last_entry = entry
        for k in duplicates:
            self.entries_dict.pop(k, None)

        # set numbers/letters for pseudo-duplicates
        for k, v in self.unique_authors_years.items():
            if 1 < len(v):
                for i, id_ in enumerate(v):
                    self.entries_dict[id_]['letter_number'] = i + 1
            else:
                id_ = v[0]
                self.entries_dict[id_]['letter_number'] = None


if __name__ == '__main__':
    n = "Orti, E. and Bredas, J. L. and Clarisse, C.".split(' and ')
    print(bib_custom.splitname("von Wright, Georg Henrik"))
