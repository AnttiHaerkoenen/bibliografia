class BibException(Exception):
    pass


class BibKeyError(KeyError, BibException):
    pass


class BibValueError(ValueError, BibException):
    pass


class BibIndexError(IndexError, BibException):
    pass
