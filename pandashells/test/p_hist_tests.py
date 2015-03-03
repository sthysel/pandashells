#! /usr/bin/env python
from mock import patch, MagicMock
from unittest import TestCase

from pandashells.bin.p_hist import main, get_input_args, validate_args, main

class GetInputArgsTests(TestCase):
    @patch('pandashells.bin.p_hist.sys.argv',
            'p.hist -c x -n 30'.split())
    def test_right_number_of_args(self):
        args = get_input_args()
        self.assertEqual(len(args.__dict__), 25)

class ValidateArgs(TestCase):
    def test_okay(self):
        # passing test means nothing raised
        args = MagicMock(quiet=False)
        cols = ['a']
        df = MagicMock(columns=['a'])
        validate_args(args, cols, df)

    @patch('pandashells.bin.p_hist.sys.stderr')
    def test_bad_cols(self, stderr_mock):
        # passing test means nothing raised
        args = MagicMock(quiet=False)
        cols = ['b']
        df = MagicMock(columns=['a'])
        with self.assertRaises(SystemExit):
            validate_args(args, cols, df)

    @patch('pandashells.bin.p_hist.sys.stderr')
    def test_bad_quiet(self, stderr_mock):
        # passing test means nothing raised
        args = MagicMock(quiet=True)
        cols = ['a', 'b']
        df = MagicMock(columns=['a', 'b'])
        with self.assertRaises(SystemExit):
            validate_args(args, cols, df)
