# -*- coding: utf-8 -*-
'''
Runner functions for integration tests
'''

# Import python libs



def failure():
    __context__['retcode'] = 1
    return False


def success():
    return True
