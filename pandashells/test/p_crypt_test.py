#! /usr/bin/env python
import copy
from contextlib import contextmanager
import json
import os
import sys
import tempfile
import shutil


from mock import patch, MagicMock
from unittest import TestCase

from pandashells.lib import config_lib
from pandashells.bin.p_crypt import main

DIR_NAME = tempfile.mkdtemp()
IN_FILE_NAME = os.path.join(self.dir_name, 'test.txt')
DECRYPTED_FILE_NAME = os.path.join(self.dir_name, 'test2.txt')
CRYPT_FILE_NAME = os.path.join(self.dir_name, 'test.txt')



@contextmanager
def mute_output():
    sys.stdout = MagicMock()
    yield
    sys.stdout = sys.__stdout__


class MainTests(TestCase):
    def setUp(self):
        self.dir_name = tempfile.mkdtemp()
        self.in_file_name = os.path.join(self.dir_name, 'test.txt')
        self.decrypted_file_name = os.path.join(self.dir_name, 'test2.txt')
        self.crypt_file_name = os.path.join(self.dir_name, 'test.txt')
        with open(self.in_file_name, 'w') as f:
            f.write('this is a test')

    def tearDown(self):
        shutil.rmtree(self.dir_name)

    @patch('pandashells.p_crypt.sys.argv')
    def test_nothing(self, argv):
        argv
        #print
        #cmd = ''.format(self.in_file_name, self.crypt_file_name)
        #os.system(cmd)
        #print
        #print cmd


    #@patch(
    #    'pandashells.bin.p_config.sys.argv',
    #    [
    #        'p.crypt',
    #        '--force_defaults',
    #    ]
    #)
    #def test_force_defaults(self):
    #    with mute_output():
    #        main()
    #    with open(config_lib.CONFIG_FILE_NAME) as config_file:
    #        config_dict = json.loads(config_file.read())
    #        self.assertEqual(config_dict, config_lib.DEFAULT_DICT)

    #@patch(
    #    'pandashells.bin.p_config.sys.argv',
    #    [
    #        'p.config',
    #        '--io_output_na_rep', '',
    #        '--io_input_type', 'table',
    #    ]
    #)
    #def test_custom(self):
    #    with mute_output():
    #        main()
    #    with open(config_lib.CONFIG_FILE_NAME) as config_file:
    #        expected_dict = copy.copy(config_lib.DEFAULT_DICT)
    #        expected_dict['io_output_na_rep'] = ''
    #        expected_dict['io_input_type'] = 'table'

    #        config_dict = json.loads(config_file.read())
    #        self.assertEqual(config_dict, expected_dict)
