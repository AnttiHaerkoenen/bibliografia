import string

from src.exceptions import *


def data_from_string(text):
    data = dict()
    cut = text.find('{')
    data['type'] = text[:cut]
    table = str.maketrans('', '', '{}')
    text = text[cut:].translate(table)
    print(text)

    return data
