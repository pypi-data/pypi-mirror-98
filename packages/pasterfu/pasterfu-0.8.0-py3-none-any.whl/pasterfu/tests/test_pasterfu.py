#! /usr/bin/env python3


import pytest
import subprocess
import webbrowser
from unittest import mock

from .. import pasterfu


@pytest.mark.skip(reason="Need to make fake database")
def test_starter_webbrowser():
    starter = pasterfu.Starter('https://about.gitlab.com/')

    with mock.patch('webbrowser.open', return_value=True) as mock_method:
        starter.start()
    mock_method.assert_called_once_with('https://about.gitlab.com/')

    # with mock.patch('subprocess.Popen', return_value=True) as mock_method:
    #     starter.start()
    # mock_method.assert_called_once_with('https://www.website.com')
