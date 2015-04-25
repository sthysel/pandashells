#! /usr/bin/env python


# standard library imports
import os
import sys
import argparse
import textwrap
import re

from pandashells.lib import module_checker_lib, arg_lib, io_lib

# import required dependencies
module_checker_lib.check_for_modules(['pandas', 'numpy'])

import pandas as pd
import numpy as np

"""
What if I had interface like this?

p.rand -n 100 -c 2 -t normal --mu --sigma --alpha -beta -N -p -k --theta --min --max
-t = uniform normal beta gamma binomial poisson (maybe divide uniform into float and int)
where mu, sigma can work for normal, gamma, beta
min max work for uniform
mu works for poisson
N, p work for binomail
alpha, beta work for uniform, beta
"""

## this dict holds info on all valid distribution types
#TYPE_LIST = [{
#    'name': 'uniform',
#    'param_list': [
#        {'name': 'low', 'val': 0},
#        {'name': 'high', 'val': 1}, ]},
#    {
#    'name': 'normal',
#    'param_list': [
#        {'name': 'loc', 'val': 0},
#        {'name': 'scale', 'val': 1}]},
#    {
#    'name': 'binomial',
#    'param_list': [
#        {'name': 'n', 'val': 1},
#        {'name': 'p', 'val': .5}]},
#    {
#    'name': 'beta',
#    'param_list': [
#        {'name': 'a', 'val': 1},
#        {'name': 'b', 'val': 1},
#    ],
#    },
#    {
#    'name': 'gamma',
#    'param_list': [
#        {'name': 'shape', 'val': 1},
#        {'name': 'scale', 'val': 1},
#    ],
#    },
#    {
#    'name': 'poisson',
#    'param_list': [{'name': 'lam', 'val': 1}],
#    },
#    {
#    'name': 'standard_t',
#    'param_list': [{'name': 'df', 'val': 1}],
#    }]




def get_samples(args):
    distribution_for = {
        'normal': {
            'function': np.random.normal,
            'kwargs': {
                'loc':  args.mu[0],
                'scale': args.sigma[0],
                'size': (args.num_samples, args.columns),
            },
        },

    }

    dist = distribution_for[args.type[0]]
    values = dist['function'](**dist['kwargs'])
    columns = ['c{}'.format(c) for c in range(args.columns[0])]
    return pd.DataFrame(values, columns=columns)


def main():
    #TODO: write docs for this
    msg = textwrap.dedent(
    """
        Return random samples from common probability distrubtions.

        Examples:
            uniform:  p.rand -n 1000 -t uniform  --min=0    --max=1   | p.hist
            normal:   p.rand -n 1000 -t normal   --mu=0     --sigma=1 | p.hist
            poisson:  p.rand -n 1000 -t poisson  --mu=1               | p.hist
            beta:     p.rand -n 1000 -t beta     --alpha=2  --beta=6  | p.hist
            gamma:    p.rand -n 1000 -t gamma    --alpha=1  --beta=1  | p.hist
            binomial: p.rand -n 1000 -t binomial --N=10     --p=0.4   | p.hist
    """)

    # read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    #options = {}
    parser.add_argument(
        '-t', '--type', nargs=1, type=str, default=['uniform'],
        choices=['uniform', 'normal', 'beta', 'gamma', 'binomial', 'poisson'],
        help='type of distribution (default=\'uniform\')')
    parser.add_argument(
        '-n', '--num_samples', nargs=1, default=[10], type=int,
        help='The number of rows to generate (default=10)')

    parser.add_argument(
        '-c', '--columns', nargs=1, default=[1], type=int,
        help='The number of columns to generate per row (default=1)')

    parser.add_argument(
        '--N', nargs=1, default=[10], type=int,
        help=(
            '(Binomial Dist) Largest possible value for random variable. '
            '(default=10)'
        )
    )

    #TODO:  maybe take the default away from this one and hard code it to adapt
    parser.add_argument(
        '--mu', nargs=1, default=[0.], type=float,
        help='(Normal, Poisson) Mean (defaults: normal:0, poisson:1')

    parser.add_argument(
        '--sigma', nargs=1, default=[1.], type=float,
        help='(Normal) standard deviation, (default: 1)')

    arg_lib.add_args(parser, 'io_out', 'example')

    # parse arguments
    args = parser.parse_args()

    df = get_samples(args)
    print
    print df.to_string()
    sys.exit()




    #parser.add_argument("-r", "--recs",
    #                    help="the number of records to generate",
    #                    nargs=1, default=[10], type=int)
    #parser.add_argument("-c", "--cols",
    #                    help="the number of columns to generate",
    #                    nargs=1, default=[1], type=int)

    #msg = 'Additional help example: p.rand normal --help'
    #subparsers = parser.add_subparsers(dest='dist_name', help=msg)

    ## add subparsers for each distribution based on TYPE_LIST info
    #for t_rec in TYPE_LIST:
    #    sub_p = subparsers.add_parser(t_rec['name'])
    #    for p_rec in t_rec['param_list']:
    #        sub_p.add_argument('--{}'.format(p_rec['name']),
    #                           default=[p_rec['val']], nargs=1,
    #                           metavar=str(p_rec['val']), type=float)

    # parse arguments
    args = parser.parse_args()

    # get the relevant distribution-type record
    t_rec = [r for r in TYPE_LIST if r['name'] == args.dist_name][0]

    # create kwargs to pass to probability function
    kwargs = {'size': (args.recs[0], args.cols[0])}
    for p_rec in t_rec['param_list']:
        kwargs[p_rec['name']] = args.__dict__[p_rec['name']][0]

    # get the probbility function from numpy.random
    prob_func = np.random.__dict__[args.dist_name]

    col_names = ['c{}'.format(nn) for nn in range(args.cols[0])]
    df = pd.DataFrame(prob_func(**kwargs), columns=col_names)

    # write dataframe to output
    io_lib.df_to_output(args, df)


if __name__ == '__main__':  # pragma: no cover
    print
    print 'running main'
    main()

