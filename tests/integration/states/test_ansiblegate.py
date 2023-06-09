# -*- coding: utf-8 -*-
'''
Test AnsibleGate State Module
'''


# Import python libraries
import os
import shutil
import tempfile
import yaml

# Import salt libraries
import salt.utils.files
import salt.utils.path

# Import testing libraries
from tests.support.case import ModuleCase
from tests.support.helpers import (
    destructiveTest,
    requires_sshd_server,
    requires_system_grains,
    flaky
)
from tests.support.mixins import SaltReturnAssertsMixin
from tests.support.runtests import RUNTIME_VARS
from tests.support.unit import skipIf


@destructiveTest
@requires_sshd_server
@skipIf(not salt.utils.path.which('ansible-playbook'), 'ansible-playbook is not installed')
class AnsiblePlaybooksTestCase(ModuleCase, SaltReturnAssertsMixin):
    '''
    Test ansible.playbooks states
    '''

    @requires_system_grains
    def setUp(self, grains=None):
        if grains.get('os_family') == 'RedHat' and grains.get('osmajorrelease') == 6:
            self.skipTest('This test hangs the test suite on RedHat 6. Skipping for now.')

        priv_file = os.path.join(RUNTIME_VARS.TMP_CONF_DIR, 'key_test')
        data = {
            'all': {
                'hosts': {
                    'localhost': {
                        'ansible_host': '127.0.0.1',
                        'ansible_port': 2827,
                        'ansible_user': RUNTIME_VARS.RUNNING_TESTS_USER,
                        'ansible_ssh_private_key_file': priv_file,
                        'ansible_ssh_extra_args': (
                            '-o StrictHostKeyChecking=false '
                            '-o UserKnownHostsFile=/dev/null '
                        )
                    },
                },
            },
        }
        self.tempdir = tempfile.mkdtemp()
        self.inventory = self.tempdir + 'inventory'
        with salt.utils.files.fopen(self.inventory, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        delattr(self, 'tempdir')
        delattr(self, 'inventory')

    @flaky
    def test_ansible_playbook(self):
        ret = self.run_state(
            'ansible.playbooks',
            name='remove.yml',
            git_repo='git://github.com/gtmanfred/playbooks.git',
            ansible_kwargs={'inventory': self.inventory}
        )
        self.assertSaltTrueReturn(ret)
        ret = self.run_state(
            'ansible.playbooks',
            name='install.yml',
            git_repo='git://github.com/gtmanfred/playbooks.git',
            ansible_kwargs={'inventory': self.inventory}
        )
        self.assertSaltTrueReturn(ret)
