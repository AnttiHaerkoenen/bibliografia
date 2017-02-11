from src.exceptions import *


class BibReader:
    def __init__(self, file, separator='\n@', encoding='utf-8', start=1):
        try:
            with open(file, 'r', encoding=encoding) as fin:
                text = fin.read()
                self.items = text.split(separator)[start:]
        except FileNotFoundError:
            print("File not found")

    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise BibTypeError("Indices must be integers")
        try:
            return self.items[item]
        except IndexError:
            raise BibIndexError

    def __str__(self):
        return str(self.items)


class BibWriter:
    def __init__(self, file):
        pass


if __name__ == '__main__':
    pass
