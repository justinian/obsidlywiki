#!/usr/bin/env python3

import click
import re

image_exts = ("jpg", "jpeg", "png", "gif", "webp")
tag_re = re.compile(r"\B#([A-Za-z_\-/]+)")
transforms = (
    (r"\B#([A-Za-z_\-/]+)", r''),
    (r'\[\[([^\|\]]+)\|([^\|\]]+)\]\]', r'[[\2|\1]]'),
    (r'!\[\[([^\]]+)\.(jpg|jpeg|png|webp)\]\]', r'<<thumb "\1.\2" left 400>>'),
    (r'!\[\[([^\]]+)\]\]', r'{{\1}}'),
    (r'\B\^[0-9a-f]+', r''),
)

def get_tags(content):
    return set(tag_re.findall(content))

def translate_article(src, dest):
    with open(src, "r") as infile:
        content = infile.read()

    tags = get_tags(content)
    if "public" not in tags: return
    tags.remove("public")

    #print(f"`{content}`")
    for pat, subst in transforms:
        content = re.sub(pat, subst, content)
        #print(f"`{content}`")

    with open(dest, "w") as outfile:
        outfile.write(content)

    if tags:
        with open(f"{dest}.meta", "w") as meta:
            meta.write(f"tags: {' '.join(tags)}\n")


def public_image(path):
    for prefix in ("images","maps"):
        if path.startswith(prefix): return True
    return False


@click.command
@click.argument("input")
@click.argument("output")
def convert(input, output):
    import os
    import shutil
    from pathlib import Path

    input = Path(input)
    output = Path(output)
    shutil.rmtree(output, ignore_errors=True)

    def files(ext):
        from glob import glob
        return glob(f"**/*.{ext}", root_dir=input, recursive=True)

    for f in files("md"):
        dest = output / f
        os.makedirs(dest.parent, exist_ok=True)
        translate_article(input / f, dest)
    
    for ext in image_exts:
        for f in [Path(f) for f in files(ext) if public_image(f)]:
            dest = output / f
            os.makedirs(dest.parent, exist_ok=True)
            shutil.copy(input / f, dest)




if __name__ == "__main__":
    convert()