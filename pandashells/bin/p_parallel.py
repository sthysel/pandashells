#! /usr/bin/env python

import sys
import argparse

from pandashells.lib import parallel_lib, arg_lib

def main():
    msg = "Tool to run shell commands in parallel.  Spawns processes "
    msg += "to concurrently run commands supplied on stdin. "

    # read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    msg = "The number of jobs to run in parallel. If not supplied, will "
    msg += "default to the number of detected cores."
    parser.add_argument('--njobs', '-n', dest='njobs', default=[None],
                        nargs=1, type=int,  help=msg)
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Enable verbose output")

    parser.add_argument("-c", "--show_commands", action="store_true",
                        default=False, help="Print commands to stdout")

    msg = "Suppress stdout, stderr, or both for all running jobs"
    parser.add_argument("-s", "--suppress",
                        choices=['stdout', 'stderr', 'both'], default=[None],
                        nargs=1, help=msg)

    # add standard arg groups
    arg_lib.addArgs(parser, 'example')

    # parse arguments
    args = parser.parse_args()

    # get the commands from stdin
    cmd_list = sys.stdin.readlines()

    # get suppression vars from args
    suppress_stdout = ('stdout' in args.suppress) or ('both' in args.suppress)
    suppress_stderr = ('stderr' in args.suppress) or ('both' in args.suppress)

    # run the commands
    parallel_lib.parallel(
        cmd_list,
        njobs=args.njobs[0],
        verbose=args.verbose,
        suppress_cmd=(not args.show_commands),
        suppress_stdout=suppress_stdout,
        suppress_stderr=suppress_stderr,
        assume_hyperthread=True)

if __name__ == '__main__':  # pragma: no cover
    main()