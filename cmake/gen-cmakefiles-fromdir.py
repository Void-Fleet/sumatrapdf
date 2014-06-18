#!/usr/bin/env python

import os

dirs = ["src", "ext", "mupdf/source"]


class DirInfo(object):
    def __init__(self, path, sources, includes):
        self.path = path
        self.sources = sources
        self.includes = includes


def is_compilable(file_name):
    ext = os.path.splitext(file_name)[-1]
    return ext in [".c", ".cpp", ".cxx", ".asm", ".rc", ".manifest"]


def is_include(file_name):
    ext = os.path.splitext(file_name)[-1]
    return ext in [".h", ".hpp", ".hxx"]


# returns DirInfo() or None if there are no sources in this dir
def build_dir_info(dir, files):
    sources = [f for f in files if is_compilable(f)]
    if len(sources) == 0:
        return None
    includes = [f for f in files if is_include(f)]
    return DirInfo(dir, sources, includes)


def dir_to_srcname(dir):
    if dir.startswith("./"):
        dir = dir[2:]
    if dir.startswith("ext/"):
        dir = dir[4:]
    dir = dir.replace("/", "_")
    dir = dir.replace("-", "_")
    return dir.upper() + "_SRC"


def quote(s):
    return '"' + s + '"'


def gen_cmake_one(di, lines):
    name = dir_to_srcname(di.path)
    s = "file (GLOB %s" % name
    lines.append(s)
    sources = di.sources
    sources.sort()
    for src in sources:
        s = quote(src)
        lines.append("\t%s" % s)
    lines.append("\t)")
    lines.append("")


def gen_cmake(arr):
    lines = []
    for di in arr:
        gen_cmake_one(di, lines)
    return "\n".join(lines)


def main():
    arr = []
    for dir, dirnames, filenames in os.walk("."):
        di = build_dir_info(dir, filenames)
        if di == None:
            continue
        arr.append(di)
    s = gen_cmake(arr)
    print(s)

if __name__ == "__main__":
    main()
