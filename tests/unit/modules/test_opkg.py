# -*- coding: utf-8 -*-
'''
    :synopsis: Unit Tests for Package Management module 'module.opkg'
    :platform: Linux
'''
# pylint: disable=import-error,3rd-party-module-not-gated
# Import Python libs

import collections
import copy

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.unit import TestCase, skipIf
from tests.support.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON
)

# Import Salt Libs
from salt.ext import six
import salt.modules.opkg as opkg
# pylint: disable=import-error,3rd-party-module-not-gated
OPKG_VIM_INFO = {
    'vim': {
        'Package': 'vim',
        'Version': '7.4.769-r0.31',
        'Status': 'install ok installed'
    }
}

OPKG_VIM_FILES = {
    'errors': [],
    'packages': {
        'vim': [
            '/usr/bin/view',
            '/usr/bin/vim.vim',
            '/usr/bin/xxd',
            '/usr/bin/vimdiff',
            '/usr/bin/rview',
            '/usr/bin/rvim',
            '/usr/bin/ex'
        ]
    }
}

INSTALLED = {
    'vim': {
        'new': '7.4',
        'old': six.text_type()
    }
}

REMOVED = {
    'vim': {
        'new': six.text_type(),
        'old': '7.4'
    }
}
PACKAGES = {
    'vim': '7.4'
}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class OpkgTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test cases for salt.modules.opkg
    '''
    def setup_loader_modules(self):  # pylint: disable=no-self-use
        '''
        Tested modules
        '''
        return {opkg: {}}

    def test_version(self):
        '''
        Test - Returns a string representing the package version or an empty string if
        not installed.
        '''
        version = OPKG_VIM_INFO['vim']['Version']
        mock = MagicMock(return_value=version)
        with patch.dict(opkg.__salt__, {'pkg_resource.version': mock}):
            self.assertEqual(opkg.version(*['vim']), version)

    def test_upgrade_available(self):
        '''
        Test - Check whether or not an upgrade is available for a given package.
        '''
        with patch('salt.modules.opkg.latest_version',
                   MagicMock(return_value='')):
            self.assertFalse(opkg.upgrade_available('vim'))

    def test_file_dict(self):
        '''
        Test - List the files that belong to a package, grouped by package.
        '''
        std_out = '\n'.join(OPKG_VIM_FILES['packages']['vim'])
        ret_value = {'stdout': std_out}
        mock = MagicMock(return_value=ret_value)
        with patch.dict(opkg.__salt__, {'cmd.run_all': mock}):
            self.assertEqual(opkg.file_dict('vim'), OPKG_VIM_FILES)

    def test_file_list(self):
        '''
        Test - List the files that belong to a package.
        '''
        std_out = '\n'.join(OPKG_VIM_FILES['packages']['vim'])
        ret_value = {'stdout': std_out}
        mock = MagicMock(return_value=ret_value)
        files = {
            'errors': OPKG_VIM_FILES['errors'],
            'files': OPKG_VIM_FILES['packages']['vim'],
        }
        with patch.dict(opkg.__salt__, {'cmd.run_all': mock}):
            self.assertEqual(opkg.file_list('vim'), files)

    def test_owner(self):
        '''
        Test - Return the name of the package that owns the file.
        '''
        paths = ['/usr/bin/vimdiff']
        mock = MagicMock(return_value='vim - version - info')
        with patch.dict(opkg.__salt__, {'cmd.run_stdout': mock}):
            self.assertEqual(opkg.owner(*paths), 'vim')

    def test_install(self):
        '''
        Test - Install packages.
        '''
        with patch('salt.modules.opkg.list_pkgs', MagicMock(side_effect=[{}, PACKAGES])):
            ret_value = {'retcode': 0}
            mock = MagicMock(return_value=ret_value)
            patch_kwargs = {
                '__salt__': {
                    'cmd.run_all': mock,
                    'pkg_resource.parse_targets': MagicMock(return_value=({'vim': '7.4'}, 'repository')),
                    'restartcheck.restartcheck': MagicMock(return_value='No packages seem to need to be restarted')
                }
            }
            with patch.multiple(opkg, **patch_kwargs):
                self.assertEqual(opkg.install('vim:7.4'), INSTALLED)

    def test_remove(self):
        '''
        Test - Remove packages.
        '''
        with patch('salt.modules.opkg.list_pkgs', MagicMock(side_effect=[PACKAGES, {}])):
            ret_value = {'retcode': 0}
            mock = MagicMock(return_value=ret_value)
            patch_kwargs = {
                '__salt__': {
                    'cmd.run_all': mock,
                    'pkg_resource.parse_targets': MagicMock(return_value=({'vim': '7.4'}, 'repository')),
                    'restartcheck.restartcheck': MagicMock(return_value='No packages seem to need to be restarted')
                }
            }
            with patch.multiple(opkg, **patch_kwargs):
                self.assertEqual(opkg.remove('vim'), REMOVED)

    def test_info_installed(self):
        '''
        Test - Return the information of the named package(s) installed on the system.
        '''
        installed = copy.deepcopy(OPKG_VIM_INFO['vim'])
        del installed['Package']
        ordered_info = collections.OrderedDict(sorted(installed.items()))
        expected_dict = {'vim': {k.lower(): v for k, v in list(ordered_info.items())}}
        std_out = '\n'.join([k + ': ' + v for k, v in list(OPKG_VIM_INFO['vim'].items())])
        ret_value = {
            'stdout': std_out,
            'retcode': 0
        }
        mock = MagicMock(return_value=ret_value)
        with patch.dict(opkg.__salt__, {'cmd.run_all': mock}):
            self.assertEqual(opkg.info_installed('vim'), expected_dict)
