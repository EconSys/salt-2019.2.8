# -*- coding: utf-8 -*-
'''
Execute a command and read the output as YAMLEX.

The YAMLEX data is then directly overlaid onto the minion's Pillar data
'''

# Import python libs

import logging

# Import salt libs
from salt.serializers.yamlex import deserialize

# Set up logging
log = logging.getLogger(__name__)


def ext_pillar(minion_id,  # pylint: disable=W0613
               pillar,  # pylint: disable=W0613
               command):
    '''
    Execute a command and read the output as YAMLEX
    '''
    try:
        command = command.replace('%s', minion_id)
        return deserialize(__salt__['cmd.run']('{0}'.format(command)))
    except Exception:
        log.critical('YAML data from %s failed to parse', command)
        return {}
