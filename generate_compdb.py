#!/usr/bin/python3

from __future__ import print_function, division

import argparse
import fnmatch
import functools
import json
import math
import multiprocessing
import os
import re
import sys


CMD_VAR_RE = re.compile(r'^\s*cmd_(\S+)\s*:=\s*(.+)\s*$', re.MULTILINE)
SOURCE_VAR_RE = re.compile(r'^\s*source_(\S+)\s*:=\s*(.+)\s*$', re.MULTILINE)


def print_progress_bar(progress):
    progress_bar = '[' + '|' * int(50 * progress) + '-' * int(50 * (1.0 - progress)) + ']'
    print('\r', progress_bar, "{0:.1%}".format(progress), end='\r', file=sys.stderr)


def parse_cmd_file(out_dir, cmdfile_path):
    with open(cmdfile_path, 'r') as cmdfile:
        cmdfile_content = cmdfile.read()

    commands = { match.group(1): match.group(2) for match in CMD_VAR_RE.finditer(cmdfile_content) }
    sources = { match.group(1): match.group(2) for match in SOURCE_VAR_RE.finditer(cmdfile_content) }

    return [{
            'directory': out_dir,
            'command': commands[o_file_name],
            'file': source,
            'output': o_file_name
        } for o_file_name, source in sources.items()]


def gen_compile_commands(out_dir, output):
    print("Building *.o.cmd file list...", file=sys.stderr)

    out_dir = os.path.abspath(out_dir)

    cmd_files = []
    for cur_dir, subdir, files in os.walk(out_dir):
        cmd_files.extend(os.path.join(cur_dir, cmdfile_name) for cmdfile_name in fnmatch.filter(files, '*.o.cmd'))

    print("Parsing *.o.cmd files...", file=sys.stderr)

    n_processed = 0
    print_progress_bar(0)

    compdb = []
    pool = multiprocessing.Pool()
    try:
        for compdb_chunk in pool.imap_unordered(functools.partial(parse_cmd_file, out_dir), cmd_files, chunksize=int(math.sqrt(len(cmd_files)))):
            compdb.extend(compdb_chunk)
            n_processed += 1
            print_progress_bar(n_processed / len(cmd_files))

    finally:
        pool.terminate()
        pool.join()

    print(file=sys.stderr)
    print("Writing %s..." % (output, ), file=sys.stderr)

    with open(output, 'w') as compdb_file:
        json.dump(compdb, compdb_file, indent=1)


def main():
    cmd_parser = argparse.ArgumentParser()
    default_out_dir = os.getcwd()
    cmd_parser.add_argument(
        '-O', '--out-dir',
        type=str, default=default_out_dir,
        help="Build output directory, default: %s (current directory)" % (default_out_dir, ))
    default_output = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compile_commands.json'))
    cmd_parser.add_argument(
        '-o', '--output',
        type=str, default=default_output,
        help="Path to resulting JSON file, default: %s" % (default_output, ))
    gen_compile_commands(**vars(cmd_parser.parse_args()))


if __name__ == '__main__':
    main()
