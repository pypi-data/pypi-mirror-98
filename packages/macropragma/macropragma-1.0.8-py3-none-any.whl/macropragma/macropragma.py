#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

import yaml

try:
    from ._metadata import __version__
except:
    __version__ = 'devel'

def menu():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument(
        "-d",
        "--directory",
        action="store",
        default="/tmp/",
        help="Root directory [project/].",
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store",
        default="False",
        help="Config file [yaml].",
    )
    _args = parser.parse_args()
    print(__name__, _args)
    return _args


def grep_check(str, greps):
    if not greps:
        return True

    for grep in greps:
        if grep not in str:
            return False
    return True


def pragma_parse(infile, substitutions, greps):
    fin_ = open(infile, "rt")
    lines_ = fin_.readlines()
    fin_.close()

    content_ = ""
    for line in lines_:
        if grep_check(line, greps) == True:
            for key, value in list(substitutions.items()):
                line = line.replace(key, value)
        content_ += line
    return content_


def store2file(data, out):
    fout_ = open(out, "wt")
    fout_.write(data)
    fout_.close()


def main():
    menu_ = menu()

    with open(menu_.config) as file:
        config_set_ = yaml.load(file, Loader=yaml.FullLoader)

    for file in config_set_:
        file_path = menu_.directory + file
        print(__name__, file_path)

        content = pragma_parse(file_path, config_set_[file]["subs"], config_set_[file]["greps"])

        store2file(content, menu_.directory + config_set_[file]["output"])


if __name__ == "__main__":
    main()
