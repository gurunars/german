#!/usr/bin/python
import os
from typing import List

import boto3
from botocore import translate


def translate(source):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=source,
        SourceLanguageCode="en",
        TargetLanguageCode="de"
    )
    return response["TranslatedText"]


def translate_file(path):
    print("Translating {}".format(path))
    with open(path) as fil:
        sources = [it.split(",")[0] for it in fil.read().split("\n") if "," in it]
    translations = []
    for src in sources:
        tr = "{},{}".format(src, translate(src))
        print("   {}".format(tr))
        translations.append(tr)

    with open(path, "w") as fil:
        fil.write("\n".join(
            translations
        ))


def validate_file(tfile):
    with open(tfile) as fil:
        lines = fil.readlines()
    errors = []
    for i, line in enumerate(lines, start=1):
        if not line:
            errors.append("Blank line @ %d" % i)
            continue
        commas = line.count(",")
        if commas == 0:
            errors.append("Line has no commas @ %d" % i)
            continue
        if line.count("  "):
            errors.append("Line has too many spaces in a row @ %d" % i)
    if errors:
        print("Errors @ %s" % tfile)
        for error in errors:
            print(error)
        print("")


def csvs(path):
    for current, _, files in os.walk(path):
        for fil in files:
            if not fil.endswith(".csv"):
                continue
            yield os.path.join(current, fil)


def reverse_csvs(path):
    with open(path) as fil:
        rev = []
        for line in fil.read().split("\n"):
            if "," not in line:
                continue
            left, right = line.split(",", maxsplit=1)
            rev.append("{},{}".format(right, left))

    with open(path.replace(".csv", ".rev.csv"), "w") as fil:
        fil.write("\n".join(rev))


def remove_prefix(prefix: str, string: str) -> str:
    if not string.startswith(prefix):
        return string
    return string[len(prefix):]



def generate_readme(paths: List[str]):
    yield "# German"
    yield ""
    for path in paths:
        yield f"[{path}](https://gurunars.com/german{path})"


def write_readme(paths: List[str]):
    with open("README.md", "w") as fil:
        for line in generate_readme(paths):
            fil.write(f"{line}\n")


def main():
    current_dir = os.path.abspath(os.curdir)
    for tfile in csvs(current_dir):
        #validate_file(tfile)
        #translate_file(tfile)
        #reverse_csvs(tfile)
        pass
    write_readme((remove_prefix(current_dir, p) for p in csvs(current_dir)))


if __name__ == "__main__":
    main()
