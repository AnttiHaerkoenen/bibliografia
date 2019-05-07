import argparse
import os


CASES = {
    'lower': str.lower,
    'upper': str.upper,
    'capitalize': str.capitalize,
}


def fix_filenames(
        files,
        replace_whitespaces=None,
        remove=None,
        case=None,
):
    for fname in files:
        new: str = fname
        if replace_whitespaces:
            new = new.replace(' ', replace_whitespaces)
        if remove:
            new = new.replace(remove, '')
        if case in CASES:
            new = CASES[case](new)
        os.rename(fname, new)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Rename files nicer")
    parser.add_argument(
        'files',
        nargs='+',
        help="Files to fix",
    )
    parser.add_argument(
        '--whitespace',
        dest='whitespace',
        default=None,
        help="Which character to replace whitespaces, default None",
    )
    parser.add_argument(
        '--remove',
        dest='remove',
        default=None,
        help="Which character to remove, default None",
    )
    parser.add_argument(
        '--case',
        dest='case',
        default=None,
        help=f"Which case to use {tuple(CASES.keys())}, default None",
    )
    args = parser.parse_args()
    fix_filenames(
        args.files,
        replace_whitespaces=args.whitespace,
        remove=args.remove,
        case=args.case,
    )
