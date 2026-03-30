from builder import Builder
from shutil import copytree, rmtree
from os import makedirs
from os.path import join, exists
from argparse import ArgumentParser
from watchfiles import run_process

parser = ArgumentParser(
    prog="generator",
    description="generates HTML from Markdown."
)
parser.add_argument('-w', '--watch', action='store_true')
parser.add_argument('-i', '--input', default='.')
parser.add_argument('-o', '--output', default='./build')
args = parser.parse_args()

src = args.input
dst = args.output
builder = Builder(src, dst)

def build():
    print("[generator] (re)generating site")
    if exists(dst):
        rmtree(dst)
    makedirs(join(dst, "posts"))

    builder.build()

    copytree("public", "build/public")
    print("[generator] done generating!")

def watch():
    print(f"[generator] watching {src}/posts, {src}/public, {src}/templates for changes")
    run_process(join(src, "posts"), join(src, "public"), join(src, "templates"), target=build)

if __name__ == '__main__':
    if (args.watch):
        watch()
    else:
        build()

