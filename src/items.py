import attr


@attr.s
class Item:
    data = attr.ib()
    style = attr.ib()
    from_string = attr.ib(True)
    author_separator = attr.ib(' and ')
    author_joiners = attr.ib(('; ', ' & '))


if __name__ == '__main__':
    pass
