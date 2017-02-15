from src import templates, string_processing
from src.exceptions import *


class Item:
    def __init__(
            self,
            data,
            style,
            from_string=True,
            author_separator=' and ',
            author_joiners=('; ', ' & ')
    ):
        self.data = string_processing.data_from_string(data) if from_string else data
        self.style = style
        self.type = self.data['type']
        self.author_separator = author_separator
        self.author_joiners = author_joiners
        self.data['authors'] = self.format_authors()
        if self.type in templates.BIBLIOGRAPHY[self.style]:
            self.template = templates.BIBLIOGRAPHY[self.style][self.type]
        else:
            self.template = templates.BIBLIOGRAPHY[self.style]['misc']
        self.citations = []

    def __str__(self):
        return self.template.format(**self.data)

    def __getitem__(self, item):
        if not isinstance(item, str):
            raise BibValueError("Keys must be strings")
        try:
            return self.data.get(item)
        except KeyError:
            raise BibKeyError

    def format_authors(self):
        if 'author' not in self.data:
            return 'Anon.'
        authors = self.data['author']
        authors = authors.split(self.author_separator)
        if len(authors) == 1:
            return authors[0]
        else:
            a = self.author_joiners[0].join(authors[:-1])
            a += self.author_joiners[1]
            a += authors[-1]
            return a


if __name__ == '__main__':
    pass
