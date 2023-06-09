# -*- coding: utf-8 -*-
'''
Integration tests for the alternatives state module
'''

# Import Python libs

import os

# Import Salt Testing libs
from tests.support.case import ModuleCase
from tests.support.unit import skipIf
from tests.support.helpers import destructiveTest
from tests.support.mixins import SaltReturnAssertsMixin

NO_ALTERNATIVES = False
if not os.path.exists('/etc/alternatives'):
    NO_ALTERNATIVES = True


@skipIf(NO_ALTERNATIVES, '/etc/alternatives does not exist on the system')
class AlterantivesStateTest(ModuleCase, SaltReturnAssertsMixin):
    @destructiveTest
    def test_install_set_and_remove(self):
        ret = self.run_state('alternatives.set', name='alt-test', path='/bin/true')
        self.assertSaltFalseReturn(ret)

        ret = self.run_state('alternatives.install', name='alt-test',
            link='/usr/local/bin/alt-test', path='/bin/true', priority=50)
        self.assertSaltTrueReturn(ret)
        self.assertSaltStateChangesEqual(ret, '/bin/true', keys=['path'])

        ret = self.run_state('alternatives.install', name='alt-test',
            link='/usr/local/bin/alt-test', path='/bin/true', priority=50)
        self.assertSaltTrueReturn(ret)
        self.assertSaltStateChangesEqual(ret, {})

        ret = self.run_state('alternatives.install', name='alt-test',
            link='/usr/local/bin/alt-test', path='/bin/false', priority=90)
        self.assertSaltTrueReturn(ret)
        self.assertSaltStateChangesEqual(ret, '/bin/false', keys=['path'])

        ret = self.run_state('alternatives.set', name='alt-test', path='/bin/false')
        self.assertSaltTrueReturn(ret)
        self.assertSaltStateChangesEqual(ret, {})

        ret = self.run_state('alternatives.set', name='alt-test', path='/bin/true')
        self.assertSaltTrueReturn(ret)
        self.assertSaltStateChangesEqual(ret, '/bin/true', keys=['path'])

        ret = self.run_state('alternatives.set', name='alt-test', path='/bin/true')
        self.assertSaltTrueReturn(ret)
        self.assertSaltStateChangesEqual(ret, {})

        ret = self.run_state('alternatives.remove', name='alt-test', path='/bin/true')
        self.assertSaltTrueReturn(ret)

        ret = self.run_state('alternatives.remove', name='alt-test', path='/bin/false')
        self.assertSaltTrueReturn(ret)
