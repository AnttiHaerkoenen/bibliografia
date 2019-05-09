from collections import OrderedDict

from src.entry import Entry


class Bibliography:
    def __init__(self, entries: dict):
        self._entries = {k, Entry(v) for k, v in entries.items()}
        self._set_letters()

    @property
    def entries_dict(self):
        return {k: e.data for k, e in self._entries.items()}

    @property
    def entries(self):
        return [e.data for e in self._entries.values()]

    def _set_letters(self):
        self._entries = sorted(lambda e: e['authors'][0][0], e['year'])
        for k, e in self._entries.items():
            if e.data.equals(last_e.data):


if __name__ == '__main__':
    pass
