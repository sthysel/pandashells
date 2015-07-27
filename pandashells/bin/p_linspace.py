#! /usr/bin/env python

# standard library imports
import sys  # NOQA import sys to allow for mocking sys.argv in tests
import argparse
import textwrap

from pandashells.lib import module_checker_lib, arg_lib, io_lib

# import required dependencies
module_checker_lib.check_for_modules(['numpy', 'pandas'])

import numpy as np
import pandas as pd


def main():
    msg = "Generate a linearly spaced set of data points."
    msg = textwrap.dedent(
        """
        Generate a linearly spaced set of data points.

        -----------------------------------------------------------------------
        Examples:

            * Generate 7 points between 1 and 10
                p.linspace 1 10 7

        -----------------------------------------------------------------------
        """
    )

    # read command line arguments
    #msg = 'p.linspace start end npoints [-h] '
    #msg += '[-o option [option ...]] [--example]'
    #parser = argparse.ArgumentParser(description=msg, usage=msg)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_out', 'example')

    msg = 'start end npoints'
    parser.add_argument("numbers", help=msg, type=str, nargs=3, metavar='')

    # parse arguments
    args = parser.parse_args()
    min_val, max_val, N = float(args.numbers[0]), float(args.numbers[1]), int(args.numbers[2])
    #args.numbers = [float(num) for num in args.numbers]

    df = pd.DataFrame({'c0': np.linspace(min_val, max_val, N)})
    #df = pd.DataFrame({'c0': np.linspace(*args.numbers)})

    # write dataframe to output
    io_lib.df_to_output(args, df)

if __name__ == '__main__':  # pragma: no cover
    main()
