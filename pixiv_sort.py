import os
import sys
import re
import requests
import html
import functools
import shutil
import argparse

import unicodedata

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
def fetch_name(id: str) -> str:
    req = requests.get(f"https://www.pixiv.net/en/artworks/{id}")
    name = re.search(br'<title.+?>(.+?)<\/title>', req.content).group(1)
    name = html.unescape(name.decode())
    name = "".join(name.split('-')[:-1]).lstrip('#').strip()

    return name

if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--src", default=".", help="The folder containing your saved files")
    args.add_argument("--done", default=".", help="Move sorted files to this folder with their original names")
    args.add_argument("--sorted", default="./sorted", help="Where the files will moved and renamed")
    args.add_argument("--gallery-file", default=None, help="Adds a blank file with the given name to every generated folder")

    args = args.parse_args()

    dir = args.src
    save_dir = args.sorted
    done_dir = args.done

    galary_file = args.gallery_file

    filepaths = os.listdir(dir)
    filepaths = [os.path.join(dir,file) for file in filepaths if file.endswith((".jpg", ".png"))]

    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(done_dir, exist_ok=True)

    for filepath in filepaths:
        try:
            id, number, ext = os.path.basename(filepath).replace(".", "_").split("_")

            name = slugify(fetch_name(id))
            dest = ""

            if os.path.exists(os.path.join(dir, f"{id}_p1.{ext}")):
                new_pos = os.path.join(save_dir, name)
                os.makedirs(new_pos, exist_ok=True)
                dest = os.path.join(new_pos, number + f".{ext}")
                if galary_file:
                    with open(os.path.join(new_pos, galary_file), "w+"):
                        pass
            else:
                dest = os.path.join(save_dir, name + f".{ext}")

            if not os.path.isfile(dest):
                os.link(filepath, dest)
            else:
                print(f"{id=} {number=} is a duplicate")
        
        except Exception as e:
            print(f"Failed to process {id=} {number=} {e=}")
            exit(-1)

    for filepath in filepaths:
        shutil.move(filepath, os.path.join(done_dir, os.path.basename(filepath)))