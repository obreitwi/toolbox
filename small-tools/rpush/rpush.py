#!/usr/bin/env python
# encoding: utf-8
"""
Usage:
    rpush [-v] [--config <cfg>] list
    rpush [-v] [--config <cfg>] clean (all|<num> ...)
    rpush [-v] [--config <cfg>] [--push] (<file> | --alias <file_in> <file_out>) ...
    rpush [-v] --help

Options:
    -h --help       Show this screen.
    --version       Show version.
    -v --verbose    Enable verbose output

    --push          Force pushing of whatever follows

    <file>          File to push to remote

    -a --alias      Indicate that the file should be renamed at remote site
    <file_in>       Input file (local)
    <file_out>      Filename of the pushed file on the server
    list            List all remote files.
    clean           Clean all remote files

    --config <cfg>  Specify config file to read. [default: ~/.config/rpushrc]

"""

from __future__ import print_function

__version__ = "0.1.3"

import os
import os.path as osp
import sys
import subprocess as sp

import random
import string

import shlex

import itertools

import logging
logging.basicConfig(
        #  format='%(asctime)s | %(funcName)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S',
        format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S',
        level = logging.INFO)

if sys.version_info < (3, 0):
    import ConfigParser as configparser
    import urllib
else:
    import configparser
    import urllib.parse as urllib

# much inspiration to be taken from:
# http://code.activestate.com/recipes/576810-copy-files-over-ssh-using-paramiko/

from docopt import docopt

def random_string(
        size=24,
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return "".join([random.choice(chars) for i in range(size)])


class RPushHandler(object):
    def __init__(self, args):
        self.args = args
        self.extra_handling()

        cfg = configparser.ConfigParser()
        cfg.read( os.path.expanduser( self.args[ "--config" ]))

        self.ssh_args = "ssh -x".split()

        section = "RPush"
        self.host       = cfg.get(section, "host")
        self.basefolder = cfg.get(section, "folder")
        self.url        = cfg.get(section, "url")
        self.www_group  = cfg.get(section, "www-group")

        self.ssh_args.append( self.host )

        if self.args["list"]:
            self.cmd_list()

        elif self.args["clean"]:
            self.cmd_clean()

        else:
            self.cmd_push()

    def extra_handling(self):
        if not self.args["--push"] and "clean" in self.args[ "<file>" ]:
            print("Please specify all or the filenumber you want to clean.")
            print("If you want to push file \"clean\" please specify push.")
            sys.exit(1)

    def cmd_push(self):
        for f_in, f_out in itertools.chain(zip(self.args[ "<file>" ], self.args[ "<file>" ]),
                                zip(self.args[ "<file_in>" ], self.args[ "<file_out>" ])):
            rfolder = random_string()
            self.run_ssh_command("mkdir "+ shlex.quote(rfolder))
            path = osp.join(rfolder, os.path.basename(f_out))
            self.run_scp_command(f_in, path)
            self.run_ssh_command("chown :{1} {0} && chmod g+r {0}".format(
                shlex.quote(path), self.www_group))

            print(self.encode_url(path))
            #  print( "{0}/{1}".format(self.url, path))

    def cmd_list(self):
        # for i,f in enumerate( self.list_complete_directory()):
        for i,f in enumerate(self.get_complete_remote_content()):
            print("[{0}]\t'{1}'\t{2}/{3}".format(
                i, f, self.url, urllib.quote(f)))

    def cmd_clean(self):
        complete_content = self.get_complete_remote_content()

        if not self.args[ "all" ]:
            to_delete = [complete_content[int(i)] for i in set(self.args["<num>"])]
        else:
            to_delete = complete_content

        for path in to_delete:
            self.remove_remote(path)

    def remove_remote(self, path):
        folder, file = osp.split(path)

        self.run_ssh_command("rm " + shlex.quote(path))
        self.run_ssh_command("rmdir " + shlex.quote(folder))

    def run_ssh_command(self, command):
        logging.debug(command)
        return self.ssh_exec(self.ssh_args
            + ["cd {0} && {1}".format(shlex.quote(self.basefolder), command)])

    def run_scp_command(self, path_from, path_to):
        logging.debug( "SCP: {0} -> {1}".format(path_from, path_to))
        return self.ssh_exec(["scp", path_from, "{0}:'{1}/{2}'".format(
            self.host, self.basefolder, path_to)])

    def ssh_exec(self, cmd):
        logging.debug(" ".join(cmd))
        proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        rc = proc.wait()
        contents, warnings = proc.communicate()
        if rc != 0:
            logging.warn(warnings)
        return contents

    def encode_url(self, path):
        return osp.join(self.url, urllib.quote(path))

    def get_complete_remote_content(self):
        return self.list_directory("*/*")

    def list_directory(self, path):
        contents = self.run_ssh_command("ls -rt {0}".format(path))

        if sys.version_info >= (3, 0):
            contents = contents.decode()

        contents = [line for line in contents.split("\n") if len(line) > 0]
        logging.debug(contents)
        return contents


if __name__ == "__main__":
    random.seed()
    arguments = docopt(__doc__, version=__version__)
    if arguments["--verbose"]:
        logging.root.setLevel(logging.DEBUG)
        #  logging.debug(arguments)
    RPushHandler(arguments)


