# -*- coding: utf-8 -*-
'''
Wheel functions for integration tests
'''

# Import python libs



def failure():
    __context__['retcode'] = 1
    return False


def success():
    return True
