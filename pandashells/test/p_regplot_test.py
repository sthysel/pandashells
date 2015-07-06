#! /usr/bin/env python
from mock import patch, MagicMock
from unittest import TestCase

import pandas as pd
from pandashells.bin.p_regplot import main, make_label

class MakeLabelTests(TestCase):
    def test_make_label_html(self):
        label = make_label(coeffs=[1, 2], savefig=['test.html'])
        self.assertEqual(label, 'y = (2) + (1) x')

    def test_make_label_tex(self):
        label = make_label(coeffs=[1, 2], savefig=['test.png'])
        self.assertEqual(label, '$y = (2) + (1) x$')


# I THINK I WANT TO SCRAP THIS AND GO WITH P.HIST STYLE TESTING
class MainTests(TestCase):
    @patch('pandashells.bin.p_regplot.argparse.ArgumentParser')
    @patch('pandashells.bin.p_regplot.arg_lib.add_args')
    @patch('pandashells.bin.p_regplot.io_lib.df_from_input')
    @patch('pandashells.bin.p_regplot.plot_lib.set_plot_styling')
    @patch('pandashells.bin.p_regplot.plot_lib.show')
    def test_plotting(
            self, show_mock, set_plot_styling_mock, df_from_input_mock,
            add_args_mock, ArgumentParserMock):
        args = MagicMock()
        args.x = ['x']
        args.y = ['y']
        args.savefig = ''
        parser = MagicMock(parse_args=MagicMock(return_value=args))
        ArgumentParserMock.return_value = parser
        df_from_input_mock.return_value = pd.DataFrame(
            {'x': [1, 2], 'y': [3, 4]})
#
        main()
#
#        add_args_mock.assert_called_with(
#            parser, 'io_in', 'xy_plotting', 'decorating', 'example')
#
#        df_from_input_mock.assert_called_with(args)
#        set_plot_styling_mock.assert_called_with(args)
#        draw_xy_mock.assert_called_with(args, 'df')
