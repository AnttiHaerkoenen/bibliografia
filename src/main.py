import os

from src import bib_io

DATA_DIR = 'data'


if __name__ == '__main__':
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    os.chdir(os.path.join(os.path.abspath(os.path.pardir), DATA_DIR))
    reader = bib_io.BibReader('bib.bib')
