"""
dumppickedversions2 test suite.
"""
import doctest
import re
import unittest
from zc.buildout import testing
from zope.testing import renormalizing

NORMALIZE_VERSION = (
    re.compile(r'[0-9]+(?:\.[0-9])+\.?(?:dev|alpha|beta|a|b)?[0-9]*'), 'N.N'
)

FLAGS = (
    doctest.ELLIPSIS |
    doctest.NORMALIZE_WHITESPACE
)


def setup(test):
    """
    Make sure we are ready to test a buildout recipe, and the develop
    version of dumppickedversions2.
    """
    testing.buildoutSetUp(test)
    testing.install_develop('buildout.dumppickedversions2', test)


def teardown(test):
    """
    Remove test artifacts.
    """
    testing.buildoutTearDown(test)


def test_suite():
    """
    Create a test suite from our doctests.
    """
    test = 'dumppickedversions2.rst'
    checker = renormalizing.RENormalizing([NORMALIZE_VERSION])
    suite = [doctest.DocFileSuite(test, optionflags=FLAGS,
                                  setUp=setup, tearDown=teardown,
                                  checker=checker)]
    return unittest.TestSuite(suite)
