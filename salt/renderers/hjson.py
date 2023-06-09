# -*- coding: utf-8 -*-
'''
hjson renderer for Salt

See the hjson_ documentation for more information

.. _hjson: http://laktak.github.io/hjson/
'''



# Import 3rd party libs
try:
    import hjson as hjson
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

# Import salt libs
from salt.ext import six


def render(hjson_data, saltenv='base', sls='', **kws):
    '''
    Accepts HJSON as a string or as a file object and runs it through the HJSON
    parser.

    :rtype: A Python data structure
    '''
    if not isinstance(hjson_data, six.string_types):
        hjson_data = hjson_data.read()

    if hjson_data.startswith('#!'):
        hjson_data = hjson_data[(hjson_data.find('\n') + 1):]
    if not hjson_data.strip():
        return {}
    return hjson.loads(hjson_data)
