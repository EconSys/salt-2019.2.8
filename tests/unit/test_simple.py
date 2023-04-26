# -*- coding: utf-8 -*-

# Import Python libs


# Import Salt Testing libs
from tests.support.unit import TestCase, expectedFailure


class SimpleTest(TestCase):
    def test_success(self):
        assert True

    @expectedFailure
    def test_fail(self):
        assert False
