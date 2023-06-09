# -*- coding: utf-8 -*-
'''
    tests.unit.utils.extend_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the salt extend script, leave templates/test alone to keep this working!
'''

# Import python libs


import os
import shutil
from datetime import date

# Import Salt Testing libs
from tests.support.unit import TestCase, skipIf
from tests.support.mock import MagicMock, patch

# Import salt libs
import tests.integration as integration
import salt.utils.extend
import salt.utils.files


class ExtendTestCase(TestCase):
    def setUp(self):
        self.starting_dir = os.getcwd()
        os.chdir(integration.CODE_DIR)
        self.out = None

    def tearDown(self):
        if self.out is not None:
            if os.path.exists(self.out):
                shutil.rmtree(self.out, True)
        os.chdir(self.starting_dir)

    @skipIf(not os.path.exists(os.path.join(integration.CODE_DIR, 'templates')),
            "Test template directory 'templates/' missing.")
    def test_run(self):
        with patch('sys.exit', MagicMock):
            out = salt.utils.extend.run('test', 'test', 'this description', integration.CODE_DIR, False)
            self.out = out
            year = date.today().strftime('%Y')
            self.assertTrue(os.path.exists(out))
            self.assertFalse(os.path.exists(os.path.join(out, 'template.yml')))
            self.assertTrue(os.path.exists(os.path.join(out, 'directory')))
            self.assertTrue(os.path.exists(os.path.join(out, 'directory', 'test.py')))
            with salt.utils.files.fopen(os.path.join(out, 'directory', 'test.py'), 'r') as test_f:
                self.assertEqual(test_f.read(), year)
