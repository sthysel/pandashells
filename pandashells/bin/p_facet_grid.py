#! /usr/bin/env python

# standard library imports
import argparse
import re
import sys  # NOQA just use this for patching in tests
import textwrap

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

# import required dependencies
module_checker_lib.check_for_modules(
    ['pandas', 'numpy', 'matplotlib', 'seaborn'])

import numpy as np
import matplotlib as mpl
import pylab as pl
import seaborn as sns

sns.set_context('talk')
CC = mpl.rcParams['axes.color_cycle']



def main():
    msg = textwrap.dedent(
        """
        Creates faceted plots using seaborn's FacetGrid capability.



        -----------------------------------------------------------------------
        Examples:

            * Example with tips
                p.facet_grid --row sex --col meal --hue sex  --map pl.scatter --args x y --kwargs 'alpha=.1' 'bins=30
        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in')

    msg = 'Different values of this variable in separate rows'
    parser.add_argument(
        '--row', nargs=1, type=str, dest='row', metavar='row', help=msg)

    msg = 'Different values of this variable in separate columns'
    parser.add_argument(
        '--col', nargs=1, type=str, dest='col', metavar='col', help=msg)

    msg = 'Different values of this variable in separate colors'
    parser.add_argument(
        '--hue', nargs=1, type=str, dest='hue', metavar='hue', help=msg)

    msg = 'The aspect ratio of each plot'
    parser.add_argument(
        '--aspect', nargs=1, type=float, dest='aspect', metavar='aspect',
        default=[2], help=msg)

    msg = 'The size of each plot (default=4)'
    parser.add_argument(
        '--size', nargs=1, type=float, dest='size', metavar='size',
        help=msg, default=[4])

    msg = 'The plotting function to use for each facet'
    parser.add_argument(
        '--map', nargs=1, type=str, dest='map', metavar='map', required=True,
        help=msg)

    msg = 'The args to pass to the plotting function'
    parser.add_argument(
        '--args', nargs='+', type=str, dest='args', metavar='args',
        required=True, help=msg)

    msg = 'The keyword arguments to pass to the plotting function'
    parser.add_argument(
        '--kwargs', nargs='+', type=str, dest='kwargs',
        metavar='kwargs', help=msg)

    #parser.add_argument(
    #    '--sharex',  type=bool, dest='sharex', default
    #    metavar='kwargs', help=msg)
    msg = 'Share x axis'
    parser.add_argument('--sharex', action='store_true', dest='sharex',
                        default=False, help=msg)

    msg = 'Share y axis'
    parser.add_argument('--sharey', action='store_true', dest='sharey',
                        default=False, help=msg)

    msg = 'x axis limits when sharex=True'
    parser.add_argument(
        '--xlim', nargs=2, type=float, dest='xlim', metavar='xlim', help=msg)

    msg = 'y axis limits when sharex=True'
    parser.add_argument(
        '--ylim', nargs=2, type=float, dest='ylim', metavar='ylim', help=msg)

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)

    facet_grid_kwargs = {
        'row': args.row[0] if args.row else None,
        'col': args.col[0] if args.col else None,
        'hue': args.hue[0] if args.hue else None,
        'aspect': args.aspect[0],
        'size': args.size[0],
        'sharex': args.sharex,
        'sharey': args.sharey,
        'xlim': args.xlim if args.xlim else None,
        'ylim': args.ylim if args.ylim else None,
    }
    grid = sns.FacetGrid(df, **facet_grid_kwargs)

    map_func_name = args.map[0]
    exec('map_func = {}'.format(map_func_name))
    map_args = args.args

    map_kwargs = {}
    for kwarg in args.kwargs:
        exec('map_kwargs.update(dict({}))'.format(kwarg))

    grid.map(map_func, *map_args, **map_kwargs)
    grid.add_legend()
    plot_lib.show(args)



#seaborn.FacetGrid(data, row=None, col=None, hue=None, col_wrap=None, sharex=True, sharey=True, size=3, aspect=1,
#                  palette=None, row_order=None, col_order=None, hue_order=None, hue_kws=None, dropna=True,
#                  legend_out=True, despine=True, margin_titles=False, xlim=None, ylim=None, subplot_kws=None,
#                  gridspec_kws=None)
if __name__ == '__main__':  # pragma: no cover
    main()
