# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Jayesh Kariya <jayeshk@saltstack.com>`
'''
# Import Python libs

import os

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.paths import TMP
from tests.support.unit import skipIf, TestCase
from tests.support.mock import (
    NO_MOCK,
    NO_MOCK_REASON,
    MagicMock,
    patch
)

# Import Salt Libs
import salt.states.beacon as beacon

SOCK_DIR = os.path.join(TMP, 'test-socks')


@skipIf(NO_MOCK, NO_MOCK_REASON)
class BeaconTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test cases for salt.states.beacon
    '''
    def setup_loader_modules(self):
        return {beacon: {}}

    # 'present' function tests: 1

    def test_present(self):
        '''
        Test to ensure a job is present in the beacon.
        '''
        beacon_name = 'ps'

        ret = {'name': beacon_name,
               'changes': {},
               'result': False,
               'comment': ''}

        mock_dict = MagicMock(side_effect=[ret, []])
        mock_mod = MagicMock(return_value=ret)
        mock_lst = MagicMock(side_effect=[{beacon_name: {}},
                                          {beacon_name: {}},
                                          {},
                                          {}])
        with patch.dict(beacon.__salt__,
                        {'beacons.list': mock_lst,
                         'beacons.modify': mock_mod,
                         'beacons.add': mock_mod}):
            self.assertDictEqual(beacon.present(beacon_name), ret)

            with patch.dict(beacon.__opts__, {'test': False}):
                self.assertDictEqual(beacon.present(beacon_name), ret)

                self.assertDictEqual(beacon.present(beacon_name), ret)

            with patch.dict(beacon.__opts__, {'test': True}):
                ret.update({'result': True})
                self.assertDictEqual(beacon.present(beacon_name), ret)

    # 'absent' function tests: 1

    def test_absent(self):
        '''
        Test to ensure a job is absent from the schedule.
        '''
        beacon_name = 'ps'

        ret = {'name': beacon_name,
               'changes': {},
               'result': False,
               'comment': ''}

        mock_mod = MagicMock(return_value=ret)
        mock_lst = MagicMock(side_effect=[{beacon_name: {}}, {}])
        with patch.dict(beacon.__salt__,
                        {'beacons.list': mock_lst,
                         'beacons.delete': mock_mod}):
            with patch.dict(beacon.__opts__, {'test': False}):
                self.assertDictEqual(beacon.absent(beacon_name), ret)

            with patch.dict(beacon.__opts__, {'test': True}):
                comt = ('ps not configured in beacons')
                ret.update({'comment': comt, 'result': True})
                self.assertDictEqual(beacon.absent(beacon_name), ret)
