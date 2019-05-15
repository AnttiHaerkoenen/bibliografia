from collections import UserDict
from collections.abc import Sequence
from abc import ABC

import bibtexparser.customization as bib_custom


def handle_authors(
        entry: dict,
) -> dict:
    """
    Sets 'author' and 'editor' each to:
        1) list of dicts of lists
        (each author passed through bibtexparser.customization.splitname)
        2) None, if 'author'/'editor' not in item_

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
    for field in 'author editor'.split():
        if field in entry:
            authors = entry[field].split(' and ')
            authors_ = []
            for au in authors:
                au_dict = bib_custom.splitname(au)
                au_dict_new = {k: (v[0] if v else '') for k, v in au_dict.items()}
                au_dict_new['first'] = au_dict['first']
                authors_.append(au_dict_new)
            entry[field] = authors_
        else:
            entry[field] = None
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
    @classmethod
    def entry_factory(cls, data_: dict):
        return next(
            c for c in cls.__subclasses__()
            if c.__name__.lower() == data_['ENTRYTYPE'].lower()
        )(data_)

    def __init__(self, data_: dict):
        data_ = bib_custom.convert_to_unicode(data_)
        for k, v in data_.items():
            if isinstance(v, str):
                data_[k] = v.replace('<br>', '').strip()
        data_ = handle_authors(data_)
        data_ = handle_pages(data_)
        data_ = bib_custom.type(data_)
        data_ = bib_custom.doi(data_)
        super().__init__(self)
        self.data = data_
        for field in set.union(self.required_fields, self.optional_fields):
            self[field] = self.data.get(field, None)

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return False
        for field in self.required_fields:
            if type(field) == set:
                if all([self[f] != self[f] for f in field]):
                    return False
            else:
                if self[field] != other[field]:
                    return False
        return True

    def __lt__(self, other):
        author, other_author = self.author_year[0], other.author_year[0]
        if not author:
            return True
        if not other_author:
            return False
        if author < other_author:
            return True
        if self['author'] == other['author']:
            return self['year'] < other['year']

    def __missing__(self, _):
        return None

    @property
    def author_year(self) -> tuple:
        author, editor = self['author'], self['editor']
        if not author or editor:
            author = tuple()
        elif not author:
            author = editor
        elif len(author) <= 3:
            author = tuple([au['last'] for au in author])
        else:
            author = author[0]['last'], 'et al.'
        return author, self.get('year', '')


class Article(Entry):
    required_fields = {
        'author',
        'title',
        'year',
        'journal',
        'volume',
    }
    optional_fields = {
        'number',
        'pages',
        'month',
        'doi',
        'note',
        'key',
        'doi',
    }


class Book(Entry):
    required_fields = {
        'title',
        'publisher',
        'year',
    }
    author_selection = frozenset('author editor'.split())
    required_fields.add(author_selection)
    optional_fields = {
        'volume',
        'number',
        'series',
        'address',
        'edition',
        'month',
        'note',
        'key',
        'url',
        'doi',
    }

    def __init__(self, data_: dict):
        super().__init__(data_)
        for field in self.author_selection:
            self[field] = self.get(field, None)


class Booklet(Entry):
    required_fields = {
        'title',
    }
    optional_fields = {
        'author',
        'howpublished',
        'address',
        'month',
        'year',
        'note',
        'key',
        'doi',
    }


class Inbook(Entry):
    required_fields = {
        'title',
        'publisher',
        'year',
    }
    author_selection = frozenset('author editor'.split())
    chapter_selection = frozenset('chapter pages'.split())
    required_fields.add(author_selection)
    required_fields.add(chapter_selection)
    optional_fields = {
        'volume',
        'number',
        'series',
        'type',
        'address',
        'edition',
        'month',
        'note',
        'doi',
    }

    def __init__(self, data_: dict):
        super().__init__(data_)
        for field in frozenset.union(self.author_selection, self.chapter_selection):
            self[field] = self.get(field, None)


class Incollection(Entry):
    required_fields = {
        'author',
        'title',
        'booktitle',
        'publisher',
        'year',
    }
    optional_fields = {
        'editor',
        'volume',
        'number',
        'series',
        'pages',
        'address',
        'month',
        'organization',
        'publisher',
        'note',
        'key',
        'doi',
    }


class Inproceedings(Entry):
    required_fields = {
        'author',
        'title',
        'booktitle',
        'year',
    }
    optional_fields = {
        'editor',
        'volume',
        'number',
        'series',
        'pages',
        'address',
        'month',
        'organization',
        'publisher',
        'note',
        'key',
        'doi',
    }


class Manual(Entry):
    required_fields = {
        'title',
    }
    optional_fields = {
        'author',
        'organization',
        'address',
        'edition',
        'month',
        'year',
        'note',
        'key',
        'doi',
    }


class Mastersthesis(Entry):
    required_fields = {
        'author',
        'title',
        'school',
        'year',
    }
    optional_fields = {
        'type',
        'address',
        'month',
        'note',
        'key',
        'doi',
    }


class Misc(Entry):
    required_fields = {}
    optional_fields = {
        'author',
        'title',
        'howpublished',
        'month',
        'year',
        'note',
        'key',
        'doi',
    }


class Phdthesis(Entry):
    required_fields = {
        'author',
        'title',
        'school',
        'year',
    }
    optional_fields = {
        'type',
        'address',
        'month',
        'note',
        'key',
        'doi',
    }


class Proceedings(Entry):
    required_fields = {
        'title',
        'year',
    }
    optional_fields = {
        'editor',
        'volume',
        'number',
        'series',
        'address',
        'month',
        'publisher',
        'organization',
        'note',
        'key',
        'doi',
    }


class Techreport(Entry):
    required_fields = {
        'author',
        'title',
        'institution',
        'year',
    }
    optional_fields = {
        'type',
        'number',
        'address',
        'month',
        'note',
        'key',
        'doi',
    }


class Unpublished(Entry):
    required_fields = {
        'author',
        'title',
        'note',
    }
    optional_fields = {
        'month',
        'year',
        'key',
        'doi',
    }


if __name__ == '__main__':
    e = Article({
        'urldate': '2015-12-04',
        'titleaddon': 'Twitter Developers',
        'abstract': 'Esri layers Tweets over maps to show live conversations for events like elections, weather, and natural disasters.',
        'url': 'https://dev.twitter.com/case-studies/esri-enriches-maps-tweets-and-streaming-api',
        'title': 'Esri enriches maps with Tweets and the Streaming API',
        'ENTRYTYPE': 'online',
        'ID': '_esri',
    })
    print(e.required_fields)
