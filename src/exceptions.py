class BibliographyBaseException(Exception):
    pass


class NotEntryError(BibliographyBaseException, TypeError):
    pass


class NotBibliographyError(BibliographyBaseException, TypeError):
    pass


class WrongEntryTypeError(BibliographyBaseException, TypeError):
    pass
