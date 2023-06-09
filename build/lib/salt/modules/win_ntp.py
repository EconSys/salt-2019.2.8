# -*- coding: utf-8 -*-
'''
Management of NTP servers on Windows

.. versionadded:: 2014.1.0
'''


# Import Python libs
import logging

# Import Salt libs
import salt.utils.platform

log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = 'ntp'


def __virtual__():
    '''
    This only supports Windows
    '''
    if not salt.utils.platform.is_windows():
        return (False, "Module win_system: module only works on Windows systems")
    return __virtualname__


def set_servers(*servers):
    '''
    Set Windows to use a list of NTP servers

    CLI Example:

    .. code-block:: bash

        salt '*' ntp.set_servers 'pool.ntp.org' 'us.pool.ntp.org'
    '''
    service_name = 'w32time'
    if not __salt__['service.status'](service_name):
        if not __salt__['service.start'](service_name):
            return False

    server_cmd = ['W32tm', '/config', '/syncfromflags:manual',
                  '/manualpeerlist:{0}'.format(' '.join(servers))]
    reliable_cmd = ['W32tm', '/config', '/reliable:yes']
    update_cmd = ['W32tm', '/config', '/update']

    for cmd in server_cmd, reliable_cmd, update_cmd:
        __salt__['cmd.run'](cmd, python_shell=False)

    if not sorted(list(servers)) == get_servers():
        return False

    __salt__['service.restart'](service_name)
    return True


def get_servers():
    '''
    Get list of configured NTP servers

    CLI Example:

    .. code-block:: bash

        salt '*' ntp.get_servers
    '''
    cmd = ['w32tm', '/query', '/configuration']
    lines = __salt__['cmd.run'](cmd, python_shell=False).splitlines()
    for line in lines:
        try:
            if line.startswith('NtpServer:'):
                _, ntpsvrs = line.rsplit(' (', 1)[0].split(':', 1)
                return sorted(ntpsvrs.split())
        except ValueError as e:
            return False
    return False
