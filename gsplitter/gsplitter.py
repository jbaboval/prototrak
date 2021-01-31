#!/usr/bin/python3

import argparse

argparser = argparse.ArgumentParser(description='Split ProtoTrak CAM files from SolidWorks CAM')

modegroup = argparser.add_mutually_exclusive_group(required=True)
modegroup.add_argument('--operation', action='store_const', dest='mode', const='operation')
modegroup.add_argument('--count', action='store_const', dest='mode', const='count')

globalgroup = argparser.add_argument_group('Global options')
globalgroup.add_argument('-r', '--renumber', help='Renumber lines in each new file')
globalgroup.add_argument('-s', '--startwith', type=int, default=0, help='N# to start new files with when renumbering')
globalgroup.add_argument('-d', '--destination', type=ascii, help='Destination directory for split files (default: input filename before extension)')
globalgroup.add_argument('-f', '--force', action='store_true', help='Remove and recreate destination if it already exists')

operationgroup = argparser.add_argument_group('Split by operation options')
operationgroup.add_argument('-n', '--starting-num', type=int, default=0, help='First O# to use in output files.')

countgroup = argparser.add_argument_group('Split by line count options')
countgroup.add_argument('-m', '--max', default=1024, type=int)

args = argparser.parse_args()


# Validate input file

# Create destination directory

# Initialize state machine

# Loop by input line

# Clean up
