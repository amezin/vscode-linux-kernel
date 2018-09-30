from __future__ import print_function, division

import fnmatch
import json
import os
import re
import sys


def print_progress_bar(progress):
    progress_bar = '[' + '|' * int(50 * progress) + '-' * int(50 * (1.0 - progress)) + ']'
    print('\r', progress_bar, "{0:.1%}".format(progress), end='\r', file=sys.stderr)


def parse_var(line, var_re, target_dict, cmdfile_path):
    match = var_re.match(line)
    if match:
        if match.group(1) in target_dict:
            print("Duplicate", match.group(0), "in", cmdfile_path, file=sys.stderr)
        else:
            target_dict[match.group(1)] = match.group(2)


CMD_VAR_RE = re.compile(r'cmd_(\S+)\s:=\s(.+)')
SOURCE_VAR_RE = re.compile(r'source_(\S+)\s:=\s(.+)')

directory = os.path.abspath(os.getcwd())
cmd_files = []
for cur_dir, subdir, files in os.walk(directory):
    cmd_files.extend(os.path.join(cur_dir, cmdfile_name) for cmdfile_name in fnmatch.filter(files, '*.o.cmd'))

o_file_command = {}
o_file_source = {}
n_processed = 0
print_progress_bar(0)

for cmdfile_path in cmd_files:
    with open(cmdfile_path, 'r') as cmdfile:
        for line in cmdfile:
            parse_var(line, CMD_VAR_RE, o_file_command, cmdfile_path)
            parse_var(line, SOURCE_VAR_RE, o_file_source, cmdfile_path)

    n_processed += 1
    print_progress_bar(n_processed / len(cmd_files))

print(file=sys.stderr)
print("Matching sources to commands...", file=sys.stderr)

compdb = [{
        'directory': directory,
        'command': o_file_command[o_file_name],
        'file': source
    } for o_file_name, source in o_file_source.items()]

print("Writing compile_commands.json...", file=sys.stderr)
with open('compile_commands.json', 'w') as compdb_file:
    json.dump(compdb, compdb_file, indent=1)
