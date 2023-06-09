# -*- coding: utf-8 -*-
'''
tests.unit.returners.pgjsonb_test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unit tests for the PGJsonb returner (pgjsonb).
'''

# Import Python libs

import logging

# Import Salt Testing libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.unit import TestCase, skipIf
from tests.support.mock import (
    MagicMock,
    NO_MOCK,
    NO_MOCK_REASON,
    patch
)

# Import Salt libs
import salt.returners.pgjsonb as pgjsonb

log = logging.getLogger(__name__)


@skipIf(NO_MOCK, NO_MOCK_REASON)
class PGJsonbCleanOldJobsTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Tests for the local_cache.clean_old_jobs function.
    '''
    def setup_loader_modules(self):
        return {pgjsonb: {'__opts__': {'keep_jobs': 1, 'archive_jobs': 0}}}

    def test_clean_old_jobs_purge(self):
        '''
        Tests that the function returns None when no jid_root is found.
        '''
        connect_mock = MagicMock()
        with patch.object(pgjsonb, '_get_serv', connect_mock):
            with patch.dict(pgjsonb.__salt__, {'config.option': MagicMock()}):
                self.assertEqual(pgjsonb.clean_old_jobs(), None)

    def test_clean_old_jobs_archive(self):
        '''
        Tests that the function returns None when no jid_root is found.
        '''
        connect_mock = MagicMock()
        with patch.object(pgjsonb, '_get_serv', connect_mock):
            with patch.dict(pgjsonb.__salt__, {'config.option': MagicMock()}):
                with patch.dict(pgjsonb.__opts__, {'archive_jobs': 1}):
                    self.assertEqual(pgjsonb.clean_old_jobs(), None)
