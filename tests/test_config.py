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

from easydingbot.config import (
    add_dingbot,
    remove_dingbot,
    configfp
)


DEFAULT_DINGBOT_CONFIG = {
                'webhook': 'https://oapi.dingtalk.com/robot/send?access_token=170d919d864e90502b48603ecbcd7646701bd66cc590f495bac1b7c5049e171e',
                'secret': 'SEC474937571de1506cdd724af0d5866f4fa2788968032a2d6d982da988bea4e5de'
            }

NEW1_DINGBOT_CONFIG = {
                'webhook': 'https://oapi.dingtalk.com/robot/send?access_token=170d919d864e90502b48603ecb4d7646701bd66cc590f495bac1b7c5049e171e',
                'secret': 'SEC474937571de1506cd3724af0d5866f4fa2788968032a2d6d982da988bea4e5de'
            }

NEW2_DINGBOT_CONFIG = {
                'webhook': 'https://oapi.dingtalk.com/robot/send?access_token=170d919d864444502b48603ecb4d7646701bd66cc590f495bac1b7c5049e171e',
                'secret': 'SEC474937571de1506cd3724af0d582224fa2788968032a2d6d982da988bea4e5de'
            }

NEW3_DINGBOT_CONFIG = {
                'webhook': 'https://oapi.dingtalk.com/robot/send?access_token=170d919d864444502b48603ecb4d7646701bd66cc590f495bac1b7c5049e171e',
                'secret': 'SEC474937571de1506cd3724af0d582224fa2788968032a2d6d982da988bea4e5de'
            }


def load_result():
    with open(configfp) as f:
        return json.load(f)


@patch('builtins.input')
def test_normal_config(input):
    input.side_effect = [DEFAULT_DINGBOT_CONFIG['webhook'], 
                         DEFAULT_DINGBOT_CONFIG['secret']]
    add_dingbot()
    result = load_result()
    assert result == {'default': DEFAULT_DINGBOT_CONFIG}
    
    input.side_effect = ['new1', 
                         NEW1_DINGBOT_CONFIG['webhook'], 
                         NEW1_DINGBOT_CONFIG['secret']]
    add_dingbot()
    result = load_result()
    assert result == {
        'default': DEFAULT_DINGBOT_CONFIG,
        'new1': NEW1_DINGBOT_CONFIG
    }
    
    input.side_effect = ['new2',
                         NEW2_DINGBOT_CONFIG['webhook'], 
                         NEW2_DINGBOT_CONFIG['secret']]
    add_dingbot()
    result = load_result()
    assert result == {
        'default': DEFAULT_DINGBOT_CONFIG,
        'new1': NEW1_DINGBOT_CONFIG,
        'new2': NEW2_DINGBOT_CONFIG
    }
    
    input.side_effect = ['new3',
                          NEW3_DINGBOT_CONFIG['webhook'], 
                          NEW3_DINGBOT_CONFIG['secret']]
    add_dingbot()
    result = load_result()
    assert result == {
        'default': DEFAULT_DINGBOT_CONFIG,
        'new1': NEW1_DINGBOT_CONFIG,
        'new2': NEW2_DINGBOT_CONFIG,
        'new3': NEW3_DINGBOT_CONFIG
    }
    
    # test remove by pass args
    assert remove_dingbot('new2', 'new3') == {
        'default': DEFAULT_DINGBOT_CONFIG,
        'new1': NEW1_DINGBOT_CONFIG
    }

    input.side_effect = ['new2',
                         NEW2_DINGBOT_CONFIG['webhook'], 
                         NEW2_DINGBOT_CONFIG['secret']]
    add_dingbot()
    result = load_result()
    assert result == {
        'default': DEFAULT_DINGBOT_CONFIG,
        'new1': NEW1_DINGBOT_CONFIG,
        'new2': NEW2_DINGBOT_CONFIG
    }
    
    # test remove by interactive cli
    input.side_effect = ['new2']
    remove_dingbot()
    result = load_result()
    assert result == {
        'default': DEFAULT_DINGBOT_CONFIG,
        'new1': NEW1_DINGBOT_CONFIG
    }
    
    os.remove(configfp)
