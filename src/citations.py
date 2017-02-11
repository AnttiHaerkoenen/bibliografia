from src import templates
from src.exceptions import *


class Citation:
    def __init__(self, data, style):
        self.data = data
        self.style = style
        self.type = data['type']
        self.template = templates.CITATION.get(self.style).get(self.type, None)

    def __str__(self):
        return self.template.format(**self.data)
