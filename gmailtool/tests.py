"""Test Suite for gmailtool

Auto discover tests in gmailtool
"""

import pkg_resources
import unittest

def test_suite(package_name='gmailtool', pattern='*_test.py'):
    """Create the test suite used for the test runer

    Discover tests and load them into a test suite.

    Args:
        package_name (str): The package we are interested in loading a test suite for
        pattern (str): The glob patten used for test discovery

    Returns:
        TestSuite: The test suite to be used for the test runner
    """

    # The egg info object is needed to get the top_level_dir value
    environment = pkg_resources.Environment()
    assert len(environment[package_name]), 'we should only have a single environment to deal with'
    this_egg_info = environment[package_name][0]

    # Find the top_level_dir, because namespaces don't work too good with unittest
    top_level_dir = this_egg_info.location

    test_loader = unittest.TestLoader()
    suite = test_loader.discover(package_name,
                                 pattern=pattern,
                                 top_level_dir=top_level_dir)
    return suite
        
