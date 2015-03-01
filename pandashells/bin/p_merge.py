#! /usr/bin/env python

# --- standard library imports
import os
import sys
import argparse
import re

from pandashells.lib import module_checker_lib, arg_lib, io_lib

# --- import required dependencies
modulesOkay = module_checker_lib.check_for_modules(['pandas'])
if not modulesOkay:
    sys.exit(1)

import pandas as pd

# =============================================================================
if __name__ == '__main__':
    msg = "Tool to merge dataframes.  Similar functionality to database "
    msg += " joins. The arguments closely parallel those of the pandas merge "
    msg += "command.  See the pandas merge documentation for more details."

    # --- read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.addArgs(parser, 'io_in', 'io_out', 'example',  # DO I REALLY NEED IO_IN ??
                    io_no_col_spec_allowed=True)

    parser.add_argument('--how', choices=['left', 'right', 'inner', 'outer'],
                        dest='how',  default=['inner'], nargs=1,
                        help="Type of join.  Default='inner'")

    msg = 'List of of columns on which to join'
    parser.add_argument('--on', nargs='+', metavar='col',
                        type=str, dest='on', help=msg)

    msg = 'List of of columns from left file to join on. '
    parser.add_argument('--left_on', nargs='+', metavar='col',
                        type=str, dest='left_on', help=msg)

    msg = 'List of of columns from right file to join on. '
    parser.add_argument('--right_on', nargs='+', metavar='col',
                        type=str, dest='right_on', help=msg)

    msg = 'List of suffixes appended to identically '
    msg += 'named columns'
    parser.add_argument('--suffixes', nargs=2, metavar='_x _y',
                        type=str, dest='suffixes', default=['_x', '_y'],
                        help=msg)

    parser.add_argument("file", help="Files to join", nargs=2, type=str,
                        metavar='file file')

    # --- parse arguments
    args = parser.parse_args()

    # --- make sure join criteria are properly specified
    if (args.left_on is None) and not (args.right_on is None):
        msg = '\nMust specify both left_on and right_on '
        msg += 'if either is specified\n\n'
        sys.stderr.write(msg)
        sys.exit(1)
    if (args.right_on is None) and not (args.left_on is None):
        msg = '\nMust specify both left_on and right_on '
        msg += 'if either is specified\n\n'
        sys.stderr.write(msg)
        sys.exit(1)
    if (args.right_on is None) and (args.left_on is None) and \
            (args.on is None):
        msg = '\nMust specify a join criteria\n\n'
        sys.stderr.write(msg)
        sys.exit(1)
    if not (args.left_on is None):
        args.on = None

    # --- get file names
    left_name, right_name = tuple(args.file)

    # --- load the dataframes
    df_left = io_lib.df_from_input(args, left_name)
    df_right = io_lib.df_from_input(args, right_name)

    # --- set default merge options
    how = args.how[0]
    on, left_on, right_on = None, None, None

    # --- set merge options for cli
    if args.on:
        on = args.on
    if args.left_on:
        left_on = args.left_on
    if args.right_on:
        right_on = args.right_on
    suffixes = args.suffixes

    # --- perform the merge
    dfj = pd.merge(df_left, df_right, how=how, on=on, left_on=left_on,
                   right_on=right_on, sort=True, suffixes=suffixes)

    # --- output the joined frame
    io_lib.df_to_output(args, dfj)
