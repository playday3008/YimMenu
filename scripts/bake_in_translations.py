# Usage `python3 bake_in_translations.py {path_to_file}`

import argparse
import glob
import json
import os
import urllib.request
import string

TRANSLATION_SOURCE = "https://raw.githubusercontent.com/YimMenu/Translations/master/"


def c_escape(to_escape: str) -> str:
    mp: str = ""
    for c in to_escape:
        if c == "\\":
            mp += "\\\\"
        elif c == "?":
            mp += "\\?"
        elif c == "'":
            mp += "\\'"
        elif c == '"':
            mp += '\\"'
        elif c == "\a":
            mp += "\\a"
        elif c == "\b":
            mp += "\\b"
        elif c == "\f":
            mp += "\\f"
        elif c == "\n":
            mp += "\\n"
        elif c == "\r":
            mp += "\\r"
        elif c == "\t":
            mp += "\\t"
        elif c == "\v":
            mp += "\\v"
        elif c in string.printable:
            mp += c
        else:
            x = "\\%03o" % c
            mp += "".join(
                x if ord(c) >= 64 else (("\\%%0%do" % (1 + ord(c) >= 8)) % c, x)
            )
    return mp


def bake_to_file(file_to_edit: str, translation_data: dict[str, str]) -> None:
    with open(file_to_edit) as file:
        file_string = file.read()
        for key in translation_data:
            escaped = c_escape(translation_data[key])
            file_string = file_string.replace(f'"{key}"', f'"{escaped}"')

        file_string = file_string.replace('"_T.data()', '"')
        file_string = file_string.replace('"_T', '"')

    with open(file_to_edit, "w") as file:
        file.write(file_string)
        print(f"Done baking in translations in: {file_to_edit}!")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Bake in translations",
        description="Bakes in translations in YimMenu source files from ex. en_US.json",
    )

    parser.add_argument(
        "target",
        type=str,
        help="File to bake translations from, accepts glob patterns (ex. ../src/**/*.cpp)",
    )
    parser.add_argument(
        "--use_local", action="store_true", help="Use local translations json"
    )
    parser.add_argument(
        "--translation_file",
        type=str,
        default="en_US.json",
        help="Name of the local translation file",
    )
    parser.add_argument(
        "--translation_language",
        type=str,
        default="en_US",
        help="Name of the remote translation language",
    )

    args = parser.parse_args()

    if args.use_local:
        with open(args.translation_file, "r") as translation_file_content:
            translation_data = json.load(translation_file_content)
    else:
        with urllib.request.urlopen(
            TRANSLATION_SOURCE + args.translation_language + ".json"
        ) as url:
            translation_data = json.load(url)

    for arg_file in glob.iglob(args.target, recursive=True):
        if not os.path.isdir(arg_file):
            print(arg_file)
            bake_to_file(arg_file, translation_data)


if __name__ == "__main__":
    main()
