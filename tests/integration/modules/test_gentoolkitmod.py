# -*- coding: utf-8 -*-

# Import python libs


# Import Salt Testing libs
from tests.support.case import ModuleCase


class GentoolkitModuleTest(ModuleCase):
    def setUp(self):
        '''
        Set up test environment
        '''
        super(GentoolkitModuleTest, self).setUp()
        ret_grain = self.run_function('grains.item', ['os'])
        if ret_grain['os'] not in 'Gentoo':
            self.skipTest('For Gentoo only')

    def test_revdep_rebuild_true(self):
        ret = self.run_function('gentoolkit.revdep_rebuild')
        self.assertTrue(ret)
