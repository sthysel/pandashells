import os
import sys
import inspect


# ############ dev only.  Comment out for production ######################
sys.path.append('../..')
# #########################################################################

from pandashells.lib import config_lib


# ============================================================================
def addArgs(parser, *args, **kwargs):
    """
    kwargs: 'io.no_col_spec_allowed'
    """

    config_dict = config_lib.get_config()
    allowedArgSet = set(
        [
            'io_in',
            'io_out',
            'example',
            'xy_plotting',
            'decorating',
        ])

    inArgSet = set(args)
    unrecognizedSet = inArgSet - allowedArgSet
    if unrecognizedSet:
        raise Exception('Unrecognized set in addArgs')

    # ------------------------------------------------------------------------
    if 'io_in' in inArgSet:
        # --- define the valid components
        io_opt_list = ['csv', 'table', 'header', 'noheader']

        # --- allow the option of supplying input column names
        if not kwargs.get('io_no_col_spec_allowed', False):
            msg = 'Overwrite column names with list of names'
            parser.add_argument('--columns', nargs='+', type=str,
                                dest='columns', metavar="col",
                                help=msg)

        # --- define the current defaults
        default_for_input = [config_dict['io_input_type'],
                             config_dict['io_input_header']]

        # --- show the current defaults in the arg parser
        msg = 'Options taken from {}'.format(repr(io_opt_list))

        parser.add_argument('-i', '--input_options', nargs='+',
                            type=str, dest='input_options', metavar='option',
                            default=default_for_input, help=msg)

    # ------------------------------------------------------------------------
    if 'io_out' in inArgSet:
        # --- define the valid components
        io_opt_list = ['csv', 'table', 'html',
                       'header', 'noheader', 'index', 'noindex']

        # --- define the current defaults
        default_for_output = [config_dict['io_output_type'],
                              config_dict['io_output_header'],
                              config_dict['io_output_index']]

        # --- show the current defaults in the arg parser
        msg = 'Options taken from {}'.format(repr(io_opt_list))
        parser.add_argument('-o', '--output_options', nargs='+',
                            type=str, dest='output_options', metavar='option',
                            default=default_for_output, help=msg)

    # ------------------------------------------------------------------------
    if 'decorating' in inArgSet:
        # --- get a list of valid plot styling info
        context_list = [t for t in config_lib.CONFIG_OPTS if
                        t[0] == 'plot_context'][0][1]
        theme_list = [t for t in config_lib.CONFIG_OPTS if
                      t[0] == 'plot_theme'][0][1]
        palette_list = [t for t in config_lib.CONFIG_OPTS if
                        t[0] == 'plot_palette'][0][1]

        # ---
        msg = "Set the x-limits for the plot"
        parser.add_argument('--xlim', nargs=2, type=float, dest='xlim',
                            metavar=('XMIN', 'XMAX'), help=msg)
        # ---
        msg = "Set the y-limits for the plot"
        parser.add_argument('--ylim', nargs=2, type=float, dest='ylim',
                            metavar=('YMIN', 'YMAX'), help=msg)
        # ---
        msg = "Set the x-label for the plot"
        parser.add_argument('--xlabel', nargs=1, type=str, dest='xlabel',
                            help=msg)
        # ---
        msg = "Set the y-label for the plot"
        parser.add_argument('--ylabel', nargs=1, type=str, dest='ylabel',
                            help=msg)
        # ---
        msg = "Set the title for the plot"
        parser.add_argument('--title', nargs=1, type=str, dest='title',
                            help=msg)
        # ---
        msg = "Specify legend location"
        parser.add_argument('--legend', nargs=1, type=str, dest='legend',
                            choices=['1', '2', '3', '4', 'best'], help=msg)
        # ---
        msg = "Specify whether hide the grid or not"
        parser.add_argument('--nogrid',  action='store_true', dest='no_grid',
                            default=False,  help=msg)

        # ---
        msg = "Specify plot context. Default = '{}' ".format(context_list[0])
        parser.add_argument('--context', nargs=1,
                            type=str, dest='plot_context',
                            default=[context_list[0]], choices=context_list,
                            help=msg)
        # ---
        msg = "Specify plot theme. Default = '{}' ".format(theme_list[0])
        parser.add_argument('--theme', nargs=1,
                            type=str, dest='plot_theme',
                            default=[theme_list[0]], choices=theme_list,
                            help=msg)
        # ---
        msg = "Specify plot palette. Default = '{}' ".format(palette_list[0])
        parser.add_argument('--palette', nargs=1,
                            type=str, dest='plot_palette',
                            default=[palette_list[0]], choices=palette_list,
                            help=msg)
        # ---
        msg = "Save the figure to this file"
        parser.add_argument('--savefig', nargs=1, type=str,
                            help=msg)

    # ------------------------------------------------------------------------
    if 'xy_plotting' in inArgSet:

        # ---
        msg = 'Column to plot on x-axis'
        parser.add_argument('-x', nargs=1, type=str, dest='x', metavar='col',
                            help=msg)
        # ---
        msg = 'List of columns to plot on y-axis'
        parser.add_argument('-y', nargs='+', type=str, dest='y',
                            metavar='col', help=msg)
        # ---
        msg = "Plot style defaults to .-"
        parser.add_argument('-s', '--style', nargs=1, type=str, dest='style',
                            default=['.-'], help=msg)

    # ------------------------------------------------------------------------
    if 'example' in inArgSet:
        msg = "Show a usage example and exit"
        parser.add_argument('--example', action='store_true', dest='example',
                            default=False,  help=msg)