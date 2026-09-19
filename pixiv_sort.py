#!/usr/bin/python
import argparse
import functools
import html
import os
import re
import shutil
import unicodedata

import requests
from tqdm import tqdm


def slugify(value, allow_unicode=True):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

@functools.cache
def fetch_name(id: str) -> (str, str):
    req = requests.get(f"https://www.pixiv.net/en/artworks/{id}")
    req.raise_for_status()
    match = re.search(br"<title[^>]*>(.*?)<\/title>", req.content)
    assert match

    try:
        raw_name = html.unescape(match.group(1).decode("utf-8"))

        matches = re.match(r"#(.+) - (.+)の(?:マンガ|イラスト)", raw_name)
        assert matches
        name, author = matches.groups()

        author = author.strip()
    except:
        print(f"{raw_name=}")
        raise

    return name, author

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--src-dir", default=".", help="The folder containing your saved files")
    arg_parser.add_argument("--done-dir", default="./done", help="Move sorted files to this folder with their original names")
    arg_parser.add_argument("--sorted", default="./sorted", help="Where the files will moved and renamed")
    arg_parser.add_argument("--gallery-file", default=None, help="Adds a blank file with the given name to every generated folder")

    args = arg_parser.parse_args()

    dir = args.src_dir
    save_dir = args.sorted
    done_dir = args.done_dir

    gallery_file = args.gallery_file

    filepaths = os.listdir(dir)
    filepaths = [os.path.join(dir,file) for file in filepaths if file.endswith((".jpg", ".png"))]

    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(done_dir, exist_ok=True)

    for filepath in (progress := tqdm(filepaths)):
        try:
            id, number, ext = os.path.basename(filepath).replace(".", "_").split("_")

            name, author = fetch_name(id)
            name = slugify(name)
            author = slugify(author)
            dest = ""
            folder_destination = os.path.join(save_dir, author, name)

            if os.path.exists(os.path.join(dir, f"{id}_p1.{ext}")) or os.path.exists(folder_destination):
                dest = os.path.join(folder_destination, number + f".{ext}")
                if gallery_file:
                    with open(os.path.join(folder_destination, gallery_file), "w+"):
                        pass
            else:
                dest = os.path.join(save_dir, author, name + f".{ext}")

            if not os.path.isfile(dest):
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                os.link(os.path.abspath(filepath), dest)
            else:
                print(f"{id=} {number=} is a duplicate")

            progress.set_description(f"{author}, {name}")
        except Exception as e:  # noqa: BLE001
            print(f"Failed to process {id=} {number=} {e=}")
        
        shutil.move(filepath, os.path.join(done_dir, os.path.basename(filepath)))