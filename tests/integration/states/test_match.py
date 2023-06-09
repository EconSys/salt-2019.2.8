# -*- coding: utf-8 -*-
'''
    :codeauthor: Pedro Algarvio (pedro@algarvio.me)


    tests.integration.states.match
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# Import python libs

import os

# Import Salt Testing libs
from tests.support.case import ModuleCase
from tests.support.paths import FILES
from tests.support.helpers import skip_if_not_root

# Import salt libs
import salt.utils.files
import salt.utils.stringutils

STATE_DIR = os.path.join(FILES, 'file', 'base')


class StateMatchTest(ModuleCase):
    '''
    Validate the file state
    '''

    @skip_if_not_root
    def test_issue_2167_ipcidr_no_AttributeError(self):
        subnets = self.run_function('network.subnets')
        self.assertTrue(len(subnets) > 0)
        top_filename = 'issue-2167-ipcidr-match.sls'
        top_file = os.path.join(STATE_DIR, top_filename)
        try:
            with salt.utils.files.fopen(top_file, 'w') as fp_:
                fp_.write(
                    salt.utils.stringutils.to_str(
                        'base:\n'
                        '  {0}:\n'
                        '    - match: ipcidr\n'
                        '    - test\n'.format(subnets[0])
                    )
                )
            ret = self.run_function('state.top', [top_filename])
            self.assertNotIn(
                'AttributeError: \'Matcher\' object has no attribute '
                '\'functions\'',
                ret
            )
        finally:
            os.remove(top_file)
