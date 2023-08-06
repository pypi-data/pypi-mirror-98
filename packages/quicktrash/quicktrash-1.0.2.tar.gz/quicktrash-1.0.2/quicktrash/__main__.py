########################################################

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("files", nargs='+')
parser.add_argument("--trashdir")

args = parser.parse_args()

########################################################

import os

def fallbacks(func):
    for val in func():
        if val is not None:
            return val

@fallbacks
def trashdir():
    yield args.trashdir
    yield os.environ.get("QUICKTRASHDIR")
    yield os.path.expanduser("~/.quicktrash")

########################################################

import sys
from . import recycle

with recycle.Trash(trashdir) as trash:
    for filepath in args.files:
        virtualpath = trash.recycle(filepath)

        if virtualpath is None:
            print(f"File not found: {filepath}", file=sys.stderr)
        else:
            print(virtualpath)

########################################################