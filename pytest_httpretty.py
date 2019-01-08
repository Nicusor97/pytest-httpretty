from distutils.version import LooseVersion
import functools

import httpretty
import pytest

__version__ = '0.2.0'


def get_marker_method(item):
    _marker_method = None
    pytest_version = LooseVersion("{}".format(pytest.__version__))
    if pytest_version < LooseVersion("4.1.0"):
        _marker_method = item.get_marker('httpretty')
    else:
        _marker_method = item.get_closest_marker('httpretty')

    return _marker_method


def pytest_configure(config):
    config.addinivalue_line('markers',
                            'httpretty: mark tests to activate HTTPretty.')


def pytest_runtest_setup(item):
    marker = get_marker_method(item)
    if marker is not None:
        httpretty.reset()
        httpretty.enable()


def pytest_runtest_teardown(item, nextitem):
    marker = get_marker_method(item)
    if marker is not None:
        httpretty.disable()


stub_get = functools.partial(httpretty.register_uri, httpretty.GET)

last_request = httpretty.last_request
