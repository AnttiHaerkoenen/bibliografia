from collections import UserDict
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
        entry['date'] = ''
        entry['year'] = ''
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


class Entry(UserDict):
    key_fields = "ENTRYTYPE author title year".split()
    extra_fields = 'number volume doi journaltitle publisher location urldate'.split()

    def __init__(self, entry: dict):
        entry = bib_custom.convert_to_unicode(entry)
        entry = handle_authors(entry)
        entry = handle_pages(entry)
        entry = handle_date(entry)
        entry = bib_custom.type(entry)
        entry = bib_custom.doi(entry)
        for field in self.extra_fields:
            if field not in entry:
                entry[field] = None
        super().__init__(self)
        self.data = entry

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return False
        return all([self[field] == other[field] for field in self.key_fields])

    @property
    def author_year(self) -> tuple:
        author = self['author']
        if not author:
            author = tuple()
        elif len(author) <= 3:
            author = tuple([au['last'] for au in author])
        else:
            author = author[0]['last'], 'et al.'
        return author, self['year']


if __name__ == '__main__':
    e = Entry({
        'urldate': '2015-12-04',
        'titleaddon': 'Twitter Developers',
        'abstract': 'Esri layers Tweets over maps to show live conversations for events like elections, weather, and natural disasters.',
        'url': 'https://dev.twitter.com/case-studies/esri-enriches-maps-tweets-and-streaming-api',
        'title': 'Esri enriches maps with Tweets and the Streaming API',
        'ENTRYTYPE': 'online',
        'ID': '_esri',
    })
    print(e.author_year)
