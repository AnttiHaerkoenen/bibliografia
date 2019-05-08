import argparse
import os
import glob


CASES = {
    'lower': str.lower,
    'upper': str.upper,
    'capitalize': str.capitalize,
}


def confirm(
        names: list,
        new_names: list,
) -> bool:
    print("Following files will be renamed:")
    for i, name in enumerate(names):
        print(f"{name} -> {new_names[i]}")
    answer = input("Are you sure? (yes/no) ")
    if answer.lower() == "yes":
        print("Renaming...")
        return True
    print("Renaming canceled.")
    return False


def fix_filenames(
        files: list,
        replace_whitespaces=None,
        remove=None,
        case=None,
):
    if '*' in files[0]:
        raise FileNotFoundError(f"No files found with {files[0]}")
    new_names = []
    for fname in files:
        new: str = fname
        if replace_whitespaces:
            new = new.replace(' ', replace_whitespaces)
        if remove:
            new = new.replace(remove, '')
        if case in CASES:
            new = CASES[case](new)
        new_names.append(new)

    if confirm(files, new_names):
        for i, f in enumerate(files):
            os.rename(f, new_names[i])


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
    files = args.files
    fix_filenames(
        files,
        replace_whitespaces=args.whitespace,
        remove=args.remove,
        case=args.case,
    )
