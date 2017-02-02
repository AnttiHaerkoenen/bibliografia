from src import templates
from src.exceptions import BibKeyError, BibValueError


class Item:
    def __init__(self, data, style):
        self.data = data
        self.style = style
        self.type = data['type']
        self.template = templates.BIBLIOGRAPHY.get(self.style).get(self.type, None)
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


if __name__ == '__main__':
    pass
