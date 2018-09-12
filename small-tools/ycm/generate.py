#!/usr/bin/env python2
# encoding: utf-8
#
# Copyright (C) 2013-2018 Oliver Breitwieser
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
    Extract compile flag information from the compile_command database.

    Turns the compile_commands.json into a dictionary {filename -> [flags]} to
    be used with the .ycm_extra_conf.py in this folder.
"""


import argparse
import json
import shlex
import os.path as osp


INVALID_FLAGS = ["-c", "-o"]


def is_invalid_flag(flag):
    return flag in INVALID_FLAGS


def extract_flags(command):
    potential_flags = shlex.split(command)

    # include compiler in flags (ycm does the same)
    flags = [potential_flags[0]]
    for f in potential_flags:
        if f.startswith("-") and not is_invalid_flag(f):
            flags.append(f)
    return flags


def extract_header_information(compile_database):
    assert isinstance(compile_database, list)

    retval = {}
    for entry in compile_database:
        filename = osp.abspath(osp.join(entry["directory"], entry["file"]))
        flags = extract_flags(entry["command"])
        retval[filename] = flags

    return retval


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input",
        type=str,
        help="Input compile_commands.json from which the header information "
             "are to be extracted.")

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="filename_to_flags.json",
        help="Output filename_to_flags.json which contains a dictionary: "
             "{ filename -> flags }")

    args = parser.parse_args()

    with open(args.input, "r") as f:
        compile_database = json.load(f)

    output = extract_header_information(compile_database)

    output_filename = args.output

    if osp.basename(args.output) == args.output:
        directory_input = osp.dirname(osp.abspath(args.input))
        output_filename = osp.join(directory_input, output_filename)

    with open(output_filename, "w") as f:
        json.dump(output, f, indent=2)

    print args.input, "->", output_filename


