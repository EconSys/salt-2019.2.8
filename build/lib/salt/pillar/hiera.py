# -*- coding: utf-8 -*-
'''
Use hiera data as a Pillar source
'''

# Import Python libs

import logging

# Import salt libs
import salt.utils.path
import salt.utils.yaml

# Import 3rd-party libs
from salt.ext import six


# Set up logging
log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only return if hiera is installed
    '''
    return 'hiera' if salt.utils.path.which('hiera') else False


def ext_pillar(minion_id,  # pylint: disable=W0613
               pillar,  # pylint: disable=W0613
               conf):
    '''
    Execute hiera and return the data
    '''
    cmd = 'hiera -c {0}'.format(conf)
    for key, val in six.iteritems(__grains__):
        if isinstance(val, six.string_types):
            cmd += ' {0}=\'{1}\''.format(key, val)
    try:
        data = salt.utils.yaml.safe_load(__salt__['cmd.run'](cmd))
    except Exception:
        log.critical('Hiera YAML data failed to parse from conf %s', conf)
        return {}
    return data
