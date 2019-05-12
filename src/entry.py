from collections import UserDict


FIELDS = "USERID author title year".split()


class Entry(UserDict):
    def __eq__(self, other: dict):
        if not other:
            return False
        if not isinstance(other, dict):
            return False
        for field in FIELDS:
            if field not in other:
                return False
        return all([self[field] == other[field] for field in FIELDS])


if __name__ == '__main__':
    pass
