# MIT License

# Copyright (c) 2020 Seniverse

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import time
import json
from unittest.mock import patch

from easydingbot import Dingbot
from easydingbot.main import configs

FAKE_CONFIG = {
        'default':
            {
                'webhook': 'https://oapi.dingtalk.com/robot/send?access_token=170d919d864e90502b48603ecbcd7646701bd66cc590f495bac1b7c5049e171e',
                'secret': 'SEC474937571de1506cdd724af0d5866f4fa2788968032a2d6d982da988bea4e5de'
            }
    }

@patch('easydingbot.main.configs', FAKE_CONFIG)
@patch('time.time')
def test_sign_and_url(time):
    time.return_value = 1606483586.285
    dingbot = Dingbot()
    dingbot.sign
    assert dingbot.signstring == 'WASfxzMjtdLTN6f0asAt4qLnI5w8xXM1EtOGHY1J1xU%3D'
    assert dingbot.url == 'https://oapi.dingtalk.com/robot/send?access_token=170d919d864e90502b48603ecbcd7646701bd66cc590f495bac1b7c5049e171e&timestamp=1606483586285&sign=WASfxzMjtdLTN6f0asAt4qLnI5w8xXM1EtOGHY1J1xU%3D'
    assert dingbot.timestamp == str(1606483586285)
