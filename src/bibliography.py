from collections import OrderedDict
from operator import attrgetter


def handle_dict(entries):
    pass


class Bibliography:
    def __init__(self, entries: dict):
        self.entries_dict = {k, handle_dict(v) for k, v in entries.items()}
        self._set_letters()

    @property
    def entries(self):
        return [e for e in self.entries_dict.values()]

    def _set_letters(self):
        pass

if __name__ == '__main__':
    pass
