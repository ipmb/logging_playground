from setuptools import setup, find_packages
import unittest


def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('logging_playground', pattern='test_*.py')
    return test_suite

setup(
    name="logging_playground",
    version=0.1,
    test_suite='setup.test_suite',
    packages=find_packages(),
)