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
    Problem:
    When relying on a compile_commands.json file completion for header files
    fails. Therefore, for header files, we use the dependency information
    (generated during compilation via the -MD switch) to find a compile unit in
    which the header file is included and use the flags of that compile unit.

    In order to speed up the process of finding flags to a given cpp-filename,
    we use a filename_to_flags.json file (generated with ./generate.py from a
    compile_commands.json file).
"""

import json
import logging
import glob2
import os
import os.path as osp
import re
import subprocess as sp

ROOT = osp.dirname(osp.abspath(__file__))

# Adjust this depending on where your build folder is
BUILD = 'build'


compilation_db = {}

HEADER_EXTENSIONS = [
        '.h',
        '.hxx',
        '.hpp',
        '.hh'
        ]

DEFAULT_FLAGS=["-xc++", "-std=c++17"]

def get_system_includes():
    output = sp.check_output("g++ -E -xc++ - -v < /dev/null", shell=True)

    output = output.splitlines()

    for first_line, line in enumerate(output):
        if line == "#include <...> search starts here:":
            first_line += 1
            break

    for num_lines, line in enumerate(output[first_line:]):
        if line == "End of search list.":
            num_lines += 1

    return output[first_line:first_line+num_lines]


def get_system_include_flags():
    return map(lambda l: "-I" + l, get_system_includes())


def init():
    global compilation_db
    #  import ycm_core
    #  compilation_db =  ycm_core.CompilationDatabase(osp.join(ROOT, BUILD))
    filename_db = osp.join(ROOT, BUILD, "filename_to_flags.json")
    with open(filename_db, "r") as f:
        compilation_db = json.load(f)
    if compilation_db is None:
        logging.error("Could not open compilation database.")


def is_header(filename):
    extension = osp.splitext(filename)[1]
    return extension in HEADER_EXTENSIONS


def get_compile_dependencies():
    return glob2.glob(osp.join(ROOT, BUILD) + "/**/*.d")


def transform_compile_unit_to_source(compile_unit):
    """
        Transform a path under the build folder into the corresponding source
        path.
    """
    build_path = osp.join(ROOT, BUILD)
    compile_path = osp.abspath(compile_unit)
    retval = osp.join(ROOT, compile_path[len(build_path)+1:])
    return retval


def get_source_file(filename):
    return transform_compile_unit_to_source(get_compile_unit(filename))


def get_compile_unit(filename):
    # This is very hacky at should be improved --obreitwi, 07-03-18 22:23:02
    return sp.check_output(["zsh", "-c",
        "head -n 1 $(grep -l {filename} {base}/**/*.d | head -n 1) |"
        "sed -e \"s/:.*$//g\" |"
        " sed -e \"s:\.[0-9]\+\.o$::g\"".format(
            base=osp.join(ROOT, BUILD).replace(" ", "\ "),
            filename=filename)]).strip()


def FlagsForFile(filename):
    if is_header(filename):
        filename = get_source_file(filename)

    flags = compilation_db.get(filename, [])

    return { "flags" : DEFAULT_FLAGS + flags }


init()
