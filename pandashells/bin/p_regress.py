#! /usr/bin/env python

# standard library imports
import os
import sys
import argparse
import re

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

# import required dependencies
module_checker_lib.check_for_modules([
    'pandas',
    'matplotlib',
    'statsmodels',
    'seaborn',
    'numpy',
    'scipy'])

import pandas as pd
import numpy as np
import scipy as scp
import matplotlib as mpl
import pylab as pl
import statsmodels.formula.api as sm
import seaborn as sns

#sns.set_context('talk')
#mpl.rcParams['figure.facecolor'] = (.98, .98, .98)
#mpl.rcParams['figure.edgecolor'] = (.98, .98, .98)

def main():
    msg = "Performs (multivariable) linear regression.  Fitting model "
    msg += "is specified using the patsy language.  Input is from stdin "
    msg += "and output is either fitting information or the input data "
    msg += "with a column containing fit results and residuals appended."

    # read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out', 'example', 'decorating')

    # specify columns to histogram
    parser.add_argument("-m", "--model", type=str, nargs=1, required=True,
                        help="The model expressed in patsy syntax")

    msg = "Return input with fit and residual appended"
    parser.add_argument("--fit", action="store_true", dest='retfit',
                        default=False, help=msg)

    parser.add_argument("--plot", action="store_true",
                        default=False, help="Make residual plots")

    parser.add_argument("-a", "--alpha", help="Set opacity",
                        nargs=1, default=[0.5], type=float)

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)

    # fit the model and add fit, resid columns
    result = sm.ols(formula=args.model[0], data=df).fit()
    df['_fit'] = result.fittedvalues
    df['_resid'] = result.resid

    # add and output the fit results if requested
    if args.retfit:
        io_lib.df_to_output(args, df)
        sys.exit(0)

    # print the fit summary
    print result.summary()
    sys.stdout.flush()

    # do plots if requested
    if args.plot:
        pl.subplot(211)
        # pl.figure()
        pl.plot(df._fit, df._resid, '.', alpha=args.alpha[0])
        # pl.xlabel('Fit Value with $R^2 = {:0.4f}$'.format(result.rsquared))
        pl.xlabel('Fit')
        pl.ylabel('Residual')
        pl.title(args.model[0])

        # pl.figure()
        pl.subplot(212)
        sns.distplot(df._resid, bins=50)
        pl.xlabel('Residual with $R^2 = {:0.4f}$'.format(result.rsquared))
        pl.ylabel('Counts')
        # pl.title(args.model[0])
        plot_lib.show(args)


    #plot_lib.set_plot_styling(args)

if __name__ == '__main__':
    main()

