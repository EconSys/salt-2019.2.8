# -*- coding: utf-8 -*-
'''
    :codeauthor: Eric Radman <ericshane@eradman.com>
'''

# Import Python libs


# Import Salt Testing libs
from tests.support.unit import skipIf, TestCase
from tests.support.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON,
)

# Import Salt libs
import salt.cloud

EXAMPLE_PROVIDERS = {
 'nyc_vcenter': {'vmware': {'driver': 'vmware',
                            'password': '123456',
                            'url': 'vca1.saltstack.com',
                            'minion': {
                                'master': 'providermaster',
                                'grains': {
                                    'providergrain': True
                                }
                            },
                            'profiles': {},
                            'user': 'root'}},
 'nj_vcenter': {'vmware': {'driver': 'vmware',
                           'password': '333',
                           'profiles': {},
                            'minion': {
                                'master': 'providermaster',
                                'grains': {
                                    'providergrain': True
                                }
                            },
                           'image': 'rhel6_64prod',
                           'url': 'vca2.saltstack.com',
                           'user': 'root'}}
}

EXAMPLE_PROFILES = {
 'nyc-vm': {'cluster': 'nycvirt',
            'datastore': 'datastore1',
            'devices': {'disk': {'Hard disk 1': {'controller': 'SCSI controller 1',
                                                 'size': 20}},
                        'network': {'Network Adapter 1': {'mac': '88:88:88:88:88:42',
                                                          'name': 'vlan50',
                                                          'switch_type': 'standard'}},
                        'scsi': {'SCSI controller 1': {'type': 'paravirtual'}}},
            'extra_config': {'mem.hotadd': 'yes'},
            'folder': 'coreinfra',
            'image': 'rhel6_64Guest',
            'minion': {
                'master': 'profilemaster',
                'grains':  {
                    'profilegrain': True
                }
            },
            'memory': '8GB',
            'num_cpus': 2,
            'power_on': True,
            'profile': 'nyc-vm',
            'provider': 'nyc_vcenter:vmware',
            'resourcepool': 'Resources'},
 'nj-vm': {'cluster': 'njvirt',
            'folder': 'coreinfra',
            'image': 'rhel6_64Guest',
            'memory': '8GB',
            'num_cpus': 2,
            'power_on': True,
            'profile': 'nj-vm',
            'provider': 'nj_vcenter:vmware',
            'resourcepool': 'Resources'},

}

EXAMPLE_MAP = {
 'nyc-vm': {'db1': {'cpus': 4,
                    'devices': {'disk': {'Hard disk 1': {'size': 40}},
                                'network': {'Network Adapter 1': {'mac': '22:4a:b2:92:b3:eb'}}},
                    'memory': '16GB',
                    'minion': {
                        'master': 'mapmaster',
                        'grains': {
                            'mapgrain': True
                        }
                    },
                    'name': 'db1'},
            'db2': {'name': 'db2',
                    'password': '456',
                    'provider': 'nj_vcenter:vmware'}},
 'nj-vm': {'db3': {'name': 'db3',
                   'password': '789',
                   }}
}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class MapConfTest(TestCase):
    '''
    Validate evaluation of salt-cloud map configuration
    '''

    def test_cloud_map_merge_conf(self):
        '''
        Ensure that nested values can be selectivly overridden in a map file
        '''
        with patch('salt.config.check_driver_dependencies', MagicMock(return_value=True)), \
                patch('salt.cloud.Map.read', MagicMock(return_value=EXAMPLE_MAP)):
            self.maxDiff = None
            opts = {'extension_modules': '/var/cache/salt/master/extmods',
                    'optimization_order': [0, 1, 2],
                    'providers': EXAMPLE_PROVIDERS, 'profiles': EXAMPLE_PROFILES}
            cloud_map = salt.cloud.Map(opts)

            merged_profile = {
             'create': {'db1': {'cluster': 'nycvirt',
                                'cpus': 4,
                                'datastore': 'datastore1',
                                'devices': {'disk': {'Hard disk 1': {'controller': 'SCSI controller 1',
                                                                     'size': 40}},
                                            'network': {'Network Adapter 1': {'mac': '22:4a:b2:92:b3:eb',
                                                                              'name': 'vlan50',
                                                                              'switch_type': 'standard'}},
                                            'scsi': {'SCSI controller 1': {'type': 'paravirtual'}}},
                                'driver': 'vmware',
                                'extra_config': {'mem.hotadd': 'yes'},
                                'folder': 'coreinfra',
                                'image': 'rhel6_64Guest',
                                'memory': '16GB',
                                'minion': {'grains': {'mapgrain': True,
                                                      'profilegrain': True,
                                                      'providergrain': True},
                                'master': 'mapmaster'},
                                'name': 'db1',
                                'num_cpus': 2,
                                'password': '123456',
                                'power_on': True,
                                'profile': 'nyc-vm',
                                'provider': 'nyc_vcenter:vmware',
                                'resourcepool': 'Resources',
                                'url': 'vca1.saltstack.com',
                                'user': 'root'},
             'db2': {'cluster': 'nycvirt',
                     'datastore': 'datastore1',
                     'devices': {'disk': {'Hard disk 1': {'controller': 'SCSI controller 1',
                                                          'size': 20}},
                                 'network': {'Network Adapter 1': {'mac': '88:88:88:88:88:42',
                                                                   'name': 'vlan50',
                                                                   'switch_type': 'standard'}},
                                 'scsi': {'SCSI controller 1': {'type': 'paravirtual'}}},
                     'driver': 'vmware',
                     'extra_config': {'mem.hotadd': 'yes'},
                     'folder': 'coreinfra',
                     'image': 'rhel6_64Guest',
                     'memory': '8GB',
                     'minion': {'grains': {'profilegrain': True,
                                           'providergrain': True},
                                'master': 'profilemaster'},
                     'name': 'db2',
                     'num_cpus': 2,
                     'password': '456',
                     'power_on': True,
                     'profile': 'nyc-vm',
                     'provider': 'nj_vcenter:vmware',
                     'resourcepool': 'Resources',
                     'url': 'vca2.saltstack.com',
                     'user': 'root'},
             'db3': {'cluster': 'njvirt',
                     'driver': 'vmware',
                     'folder': 'coreinfra',
                     'image': 'rhel6_64Guest',
                     'memory': '8GB',
                     'minion': {'grains': {'providergrain': True},
                                'master': 'providermaster'},
                     'name': 'db3',
                     'num_cpus': 2,
                     'password': '789',
                     'power_on': True,
                     'profile': 'nj-vm',
                     'provider': 'nj_vcenter:vmware',
                     'resourcepool': 'Resources',
                     'url': 'vca2.saltstack.com',
                     'user': 'root'}}
            }

            # what we assert above w.r.t db2 using nj_vcenter:vmware provider:
            # - url is from the overriden nj_vcenter provider, not nyc_vcenter
            # - image from provider is still overridden by the nyc-vm profile
            # - password from map override is still overriding both the provider and profile password
            #
            # what we assert above about grain handling ( and provider/profile/map data in general )
            # - provider grains are able to be overridden by profile data
            # - provider grain sare overridden by map data
            # - profile data is overriden by map data
            # ie, the provider->profile->map inheritance works as expected
            map_data = cloud_map.map_data()
            self.assertEqual(map_data, merged_profile)
