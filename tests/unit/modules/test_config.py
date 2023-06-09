# -*- coding: utf-8 -*-

# Import Python libs


# Import Salt Testing libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.unit import skipIf, TestCase
from tests.support.mock import NO_MOCK, NO_MOCK_REASON, patch

# Import Salt libs
import salt.modules.config as config

DEFAULTS = {
    'test.option.all': 'value of test.option.all in DEFAULTS',
    'test.option': 'value of test.option in DEFAULTS'
}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class TestModulesConfig(TestCase, LoaderModuleMockMixin):

    def setup_loader_modules(self):
        return {
            config: {
                '__opts__': {
                    'test.option.all': 'value of test.option.all in __opts__'
                },
                '__pillar__': {
                    'test.option.all': 'value of test.option.all in __pillar__',
                    'master': {
                        'test.option.all': 'value of test.option.all in master'
                    }
                }
            }
        }

    def test_defaults_only_name(self):
        with patch.dict(config.DEFAULTS, DEFAULTS):
            opt_name = 'test.option'
            opt = config.option(opt_name)
            self.assertEqual(opt, config.DEFAULTS[opt_name])

    def test_omits(self):
        with patch.dict(config.DEFAULTS, DEFAULTS):
            opt_name = 'test.option.all'
            opt = config.option(opt_name,
                                omit_opts=False,
                                omit_master=True,
                                omit_pillar=True)

            self.assertEqual(opt, config.__opts__[opt_name])

            opt = config.option(opt_name,
                                omit_opts=True,
                                omit_master=True,
                                omit_pillar=False)

            self.assertEqual(opt, config.__pillar__[opt_name])
            opt = config.option(opt_name,
                                omit_opts=True,
                                omit_master=False,
                                omit_pillar=True)

            self.assertEqual(
                opt, config.__pillar__['master'][opt_name])
