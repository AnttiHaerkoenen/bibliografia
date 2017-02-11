from src import templates, string_processing
from src.exceptions import *


class Item:
    def __init__(self, data, style, from_string=True):
        self.data = string_processing.data_from_string(data) if from_string else data
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
