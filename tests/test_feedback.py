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

import time
from unittest.mock import patch
from easydingbot import feedback


@patch('easydingbot.main.Dingbot')
def test_feedback_normal(mock_dingbot):
    dingbot = mock_dingbot.return_value
    dingbot.send_msg.return_value = '{"errcode":0,"errmsg":"ok"}'

    @feedback()
    def some_task_normal():
        time.sleep(2)

    assert some_task_normal() == ('{"errcode":0,"errmsg":"ok"}',
                                  '{"errcode":0,"errmsg":"ok"}')


@patch('easydingbot.main.Dingbot')
def test_feedback_failed(mock_dingbot):
    dingbot = mock_dingbot.return_value
    dingbot.send_msg.return_value = '{"errcode":0,"errmsg":"ok"}'

    @feedback()
    def some_task_failed():
        time.sleep(2)
        1 / 0

    assert some_task_failed() == ('{"errcode":0,"errmsg":"ok"}',
                                    '{"errcode":0,"errmsg":"ok"}',
                                    'ZeroDivisionError: division by zero')
