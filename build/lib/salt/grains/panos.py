# -*- coding: utf-8 -*-
'''
Generate baseline proxy minion grains for panos hosts.

'''

# Import Python Libs

import logging

# Import Salt Libs
import salt.utils.platform
import salt.proxy.panos

__proxyenabled__ = ['panos']
__virtualname__ = 'panos'

log = logging.getLogger(__file__)

GRAINS_CACHE = {'os_family': 'panos'}


def __virtual__():
    try:
        if salt.utils.platform.is_proxy() and __opts__['proxy']['proxytype'] == 'panos':
            return __virtualname__
    except KeyError:
        pass

    return False


def panos(proxy=None):
    if not proxy:
        return {}
    if proxy['panos.initialized']() is False:
        return {}
    return {'panos': proxy['panos.grains']()}
