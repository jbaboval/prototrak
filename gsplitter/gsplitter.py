#!/usr/bin/python3

import argparse
import codecs
import os
import re
import shutil

def p_new_file(outfile, line_type, args, outwrites):
    if (outfile is None):
        return True

    if (args.mode == 'operation' and line_type in ["opcomment", "operation"] and outwrites > 0):
        return True

    if (args.mode == 'count' and outwrites > args.max):
        return True

    return False

# airquotes parser
# Returns (<Nnum>, <type>, <contents>)
def parse_line(line):
    line = line.lstrip()

    if (line is None or len(line) == 0):
        return (None, 'blank', "\r\n")

    if (re.match("^[(]OPERATION", line)):
        return (None, 'opcomment', line)

    (n, n_number, contents) = re.match("^(N(\d+))?\s*(.*)$", line).groups()
    if (contents[0] == 'O'):
        return (n_number, 'operation', contents)

    return (n_number, 'regular', contents)

argparser = argparse.ArgumentParser(description='Split ProtoTrak CAM files from SolidWorks CAM')

modegroup = argparser.add_mutually_exclusive_group(required=True)
modegroup.add_argument('--operation', action='store_const', dest='mode', const='operation')
modegroup.add_argument('--count', action='store_const', dest='mode', const='count')

globalgroup = argparser.add_argument_group('Global options')
globalgroup.add_argument('-r', '--renumber', action='store_true', help='Renumber lines in each new file')
globalgroup.add_argument('-S', '--strip', action='store_true', help='Strip Nnumbers')
globalgroup.add_argument('-s', '--startwith', type=int, default=0, help='N# to start new files with when renumbering')
globalgroup.add_argument('-d', '--destination', type=ascii, help='Destination directory for split files (default: input filename before extension)')
globalgroup.add_argument('-f', '--force', action='store_true', help='Remove and recreate destination if it already exists')

operationgroup = argparser.add_argument_group('Split by operation options')
operationgroup.add_argument('-n', '--starting-num', type=int, default=0, help='First O# to use in output files.')

countgroup = argparser.add_argument_group('Split by line count options')
countgroup.add_argument('-m', '--max', default=1024, type=int)

# ProtoTrak CAM files are for MS-DOS 5
argparser.add_argument('inputfile', type=argparse.FileType('r', encoding='cp437'))
args = argparser.parse_args()

# Validate input file
(path, filename) = os.path.split(args.inputfile.name)
(operation, extension) = os.path.splitext(filename)

if ((filename != '<stdin>') and (extension.lower() != '.cam')):
    raise Exception("Only .cam files are supported")

if ((filename == '<stdin>') and (args.destination is None)):
    raise Exception("Destination must be set if input is <stdin>")

if (args.destination is None):
    args.destination = operation

# Create destination directory

outpath = os.path.join(path, args.destination)
if (os.path.exists(outpath)):
    if (args.force):
        shutil.rmtree(outpath)
    else:
        raise Exception("Destination path already exists (and --force was not specified)")

os.mkdir(outpath)

# Initialize state machine

line_number = 1
operation = args.startwith
outfile = None
outwrites = 0

# Loop by input line

for line in args.inputfile:
    (n_number, line_type, contents) = parse_line(line)

    if (p_new_file(outfile, line_type, args, outwrites)):
        if (outfile is not None):
            outfile.close()
        filename = f"{operation:03}.cam"
        outfile = codecs.open(os.path.join(outpath, filename), mode="w+", encoding='cp437')
        outwrites = 0
        line_number = 1
        outfile.write(f"O{operation:03}\r\n")
        operation += 1

    if (n_number is not None):
        if (not args.strip):
            if (args.renumber):
                outfile.write(f"N{line_number:04} ")
            else:
                outfile.write(f"N{n_number:04} ")
        line_number += 1

    if (line_type in ['regular', 'opcomment']):
        outfile.write(contents)
        outwrites += 1

    outfile.write("\r\n")

# Clean up

if (outfile is not None):
    outfile.close()


