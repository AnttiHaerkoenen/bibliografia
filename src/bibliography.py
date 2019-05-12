from collections import OrderedDict
from collections.abc import Sequence

import bibtexparser.customization as bib_custom

from .entry import Entry


class Bibliography:
    def __init__(self, entries: dict):
        self.entries_dict: OrderedDict = OrderedDict(
            {k: Entry(v) for k, v in entries.items()}
        )
        self._handle_duplicates()

    @property
    def entries(self) -> list:
        return [e for e in self.entries_dict.values()]

    @property
    def authors_years_dict(self) -> dict:
        return {k: entry.author_year for k, entry in self.entries_dict.items()}

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
            key=lambda key_val: key_val[1].author_year,
        ))

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
