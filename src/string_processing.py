from src.exceptions import *


def data_from_string(text):
    data = dict()
    cut = text.find('{')
    data['type'] = text[:cut]
    table = str.maketrans('', '', '{}')
    text = text[cut:].translate(table)
    text = text.split(',\n')
    data['id'] = text[0]

    for line in text[1:]:
        k, v = line.split(' = ')
        data[k] = v

    return data
