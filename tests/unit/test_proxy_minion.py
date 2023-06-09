# -*- coding: utf-8 -*-
'''
    :codeauthor: Gareth J. Greenaway <gareth@saltstack.com>
'''

# Import python libs

import copy

import logging
import tornado
import tornado.testing

# Import Salt Testing libs
from tests.support.unit import TestCase, skipIf
from tests.support.mock import NO_MOCK, NO_MOCK_REASON
from tests.support.mixins import AdaptedConfigurationTestCaseMixin

# Import salt libs
import salt.minion
import salt.syspaths


log = logging.getLogger(__name__)
__opts__ = {}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class ProxyMinionTestCase(TestCase, AdaptedConfigurationTestCaseMixin):
    def test_post_master_init_metaproxy_called(self):
        '''
        Tests that when the _post_master_ini function is called, _metaproxy_call is also called.
        '''
        mock_opts = salt.config.DEFAULT_MINION_OPTS
        mock_jid_queue = [123]
        proxy_minion = salt.minion.ProxyMinion(mock_opts, jid_queue=copy.copy(mock_jid_queue), io_loop=tornado.ioloop.IOLoop())
        try:
            ret = proxy_minion._post_master_init('dummy_master')
            self.assert_called_once(salt.minion._metaproxy_call)
        finally:
            proxy_minion.destroy()

    def test_handle_decoded_payload_metaproxy_called(self):
        '''
        Tests that when the _handle_decoded_payload function is called, _metaproxy_call is also called.
        '''
        mock_opts = salt.config.DEFAULT_MINION_OPTS
        mock_data = {'fun': 'foo.bar',
                     'jid': 123}
        mock_jid_queue = [123]
        proxy_minion = salt.minion.ProxyMinion(mock_opts, jid_queue=copy.copy(mock_jid_queue), io_loop=tornado.ioloop.IOLoop())
        try:
            ret = proxy_minion._handle_decoded_payload(mock_data).result()
            self.assertEqual(proxy_minion.jid_queue, mock_jid_queue)
            self.assertIsNone(ret)
            self.assert_called_once(salt.minion._metaproxy_call)
        finally:
            proxy_minion.destroy()

    def test_handle_payload_metaproxy_called(self):
        '''
        Tests that when the _handle_payload function is called, _metaproxy_call is also called.
        '''
        mock_opts = salt.config.DEFAULT_MINION_OPTS
        mock_data = {'fun': 'foo.bar',
                     'jid': 123}
        mock_jid_queue = [123]
        proxy_minion = salt.minion.ProxyMinion(mock_opts, jid_queue=copy.copy(mock_jid_queue), io_loop=tornado.ioloop.IOLoop())
        try:
            ret = proxy_minion._handle_decoded_payload(mock_data).result()
            self.assertEqual(proxy_minion.jid_queue, mock_jid_queue)
            self.assertIsNone(ret)
            self.assert_called_once(salt.minion._metaproxy_call)
        finally:
            proxy_minion.destroy()
