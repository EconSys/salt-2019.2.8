# -*- coding: utf-8 -*-
'''
The local returner is used to test the returner interface, it just prints the
return data to the console to verify that it is being passed properly

To use the local returner, append '--return local' to the salt command. ex:

.. code-block:: bash

    salt '*' test.ping --return local
'''

# Import python libs



def returner(ret):
    '''
    Print the return data to the terminal to verify functionality
    '''
    print(ret)


def event_return(event):
    '''
    Print event return data to the terminal to verify functionality
    '''

    print(event)
