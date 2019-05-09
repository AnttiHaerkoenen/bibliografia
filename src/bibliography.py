def _handle_entries(entries: dict):
    return dict()


class Bibliography:
    def __init__(self, entries: dict):
        self._entries: dict = _handle_entries(entries)
        self._get_letters()

    @property
    def entries_dict(self):
        return {k: e.data for k, e in self._entries.items()}

    @property
    def entries(self):
        return [e.data for e in self._entries.values()]

    def _get_letters(self):
        pass


if __name__ == '__main__':
    pass
