import attr


@attr.s
class Citation:
    data = attr.ib()
    style = attr.ib()
