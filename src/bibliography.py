from collections import OrderedDict

import bibtexparser.customization as bib_custom

from .entries import Entry
from .exceptions import NotBibliographyError, WrongEntryTypeError


class Bibliography:
    def __init__(self, entries: dict or list):
        if isinstance(entries, dict):
            self._data: OrderedDict = OrderedDict(
                {k: Entry.entry_factory(v) for k, v in entries.items()}
            )
        elif isinstance(entries, list):
            self._data: OrderedDict = OrderedDict(
                {e['ID']: Entry.entry_factory(e) for e in entries}
            )
        else:
            raise WrongEntryTypeError(f"Expected list or dict, got {type(entries)}")
        self._handle_duplicates()

    def __len__(self):
        return len(self._data)

    def __add__(self, other):
        if not isinstance(other, Bibliography):
            raise NotBibliographyError()
        for k, v in other._data.items():
            if k in self._data:
                self._data[k].update(v)
            else:
                self._data[k] = v
        self.sort()
        self._handle_duplicates()
        return self

    def __sub__(self, other):
        if not isinstance(other, Bibliography):
            raise NotBibliographyError()
        for k, v in other._data.items():
            if self._data[k] == v:
                self._data.pop(k, None)
        self.sort()
        self._handle_duplicates()
        return self

    def __iter__(self):
        raise NotImplementedError("Use entries or entries_dict")

    def __contains__(self, item):
        return any((entry == item) for entry in self.entries)

    @property
    def entries(self) -> list:
        return [e for e in self._data.values()]

    @property
    def entries_dict(self):
        return self._data

    @property
    def authors_years_dict(self) -> dict:
        return {k: entry.author_year for k, entry in self._data.items()}

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
        self._data = OrderedDict(sorted(
            self._data.items(),
            key=lambda key_val: key_val[1]
        ))

    def _handle_duplicates(self):
        self.sort()

        # delete duplicates
        duplicates = []
        last_entry = object()
        for k, entry in self._data.items():
            if entry == last_entry:
                duplicates.append(k)
            last_entry = entry
        for k in duplicates:
            self._data.pop(k, None)

        # set numbers/letters for pseudo-duplicates
        for k, v in self.unique_authors_years.items():
            if 1 < len(v):
                for i, id_ in enumerate(v):
                    self._data[id_]['letter_number'] = i + 1
            else:
                id_ = v[0]
                self._data[id_]['letter_number'] = None


if __name__ == '__main__':
    n = "Orti, E. and Bredas, J. L. and Clarisse, C.".split(' and ')
    print(bib_custom.splitname("von Wright, Georg Henrik"))
