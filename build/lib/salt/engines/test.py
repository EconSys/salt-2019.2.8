# -*- coding: utf-8 -*-
'''
A simple test engine, not intended for real use but as an example
'''

# Import python libs

import logging

# Import salt libs
import salt.utils.event
import salt.utils.json

log = logging.getLogger(__name__)


def start():
    '''
    Listen to events and write them to a log file
    '''
    if __opts__['__role'] == 'master':
        event_bus = salt.utils.event.get_master_event(
                __opts__,
                __opts__['sock_dir'],
                listen=True)
    else:
        event_bus = salt.utils.event.get_event(
            'minion',
            transport=__opts__['transport'],
            opts=__opts__,
            sock_dir=__opts__['sock_dir'],
            listen=True)
        log.debug('test engine started')

    while True:
        event = event_bus.get_event()
        jevent = salt.utils.json.dumps(event)
        if event:
            log.debug(jevent)
