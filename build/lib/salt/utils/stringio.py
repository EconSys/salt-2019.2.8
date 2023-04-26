# -*- coding: utf-8 -*-
'''
Functions for StringIO objects
'''



# Import 3rd-party libs
from salt.ext import six

# Not using six's fake cStringIO since we need to be able to tell if the object
# is readable, and this can't be done via what six exposes.
if six.PY2:
    import io
    import io
    readable_types = (io.StringIO, io.InputType)
    writable_types = (io.StringIO, io.OutputType)
else:
    import io
    readable_types = (io.StringIO,)
    writable_types = (io.StringIO,)


def is_stringio(obj):
    return isinstance(obj, readable_types)


def is_readable(obj):
    if six.PY2:
        return isinstance(obj, readable_types)
    else:
        return isinstance(obj, readable_types) and obj.readable()


def is_writable(obj):
    if six.PY2:
        return isinstance(obj, writable_types)
    else:
        return isinstance(obj, writable_types) and obj.writable()
