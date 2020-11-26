# easydingbot
[![PyPI version](https://badge.fury.io/py/easydingbot.svg)](https://badge.fury.io/py/easydingbot)

Easydingbot is a package to make dingbot easily to use.

## Installation
You can install easydingbot by `pip`
```shell
$ pip install easydingbot
```
or
```
$ pip install git+https://github.com/seniverse/easydingbot@main
```
## Configuration
You must inject your dingbot's **webhook** and **secret-code** into configuration before using easydingbot.   
Please see [dingbot's documentation](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq) to learn how to get webhook and secret-code.   
After that, you can inject them by `easydingbot add-dingbot` command:
```shell
$ easydingbot add-dingbot
It's first time to set dingbot, we will use "default" as the first dingbot id.
Please input the webhook string ("q" to quit) >
Please input the secret string ("q" to quit) > 
```
**Note that it won't show the webhook and secret string that you typed because we regard them as password.** Then you can list all dingbots already in configuration by `easydingbot ls-dingbot` command:
```shell
$ easydingbot ls-dingbot
There are 1 dingbots in config as follow:
  * default
```
If you want to check whether this configuration can work well, you can use `easydingbot touch` command to test for once:
```
$ easydingbot touch
Dingbot of default's status is normal.
```
The command above is equal to `easydingbot touch default`.   
If you want another's dingbot config, you can pass a new name(dingbot id) to `easydingbot add-dingbot`:
```shell
$ easydingbot add-dingbot another
Please input the webhook string ("q" to quit) >
Please input the secret string ("q" to quit) > 
```

Then you will have two dingbot in your configuration.
```
$ easydingbot ls-dingbot
There are 2 dingbots in config as follow:
  * another
  * default
```
And you can assign their ids to touch.
```
$ easydingbot touch another
Dingbot of another status is normal.
```
If you find your touched result is abnormal and suspect you inputed wrong webhook or secret-code, you can use `easydingbot add-dingbot` again, type the same dingbot id to overwrite it.   
If you want to remove one of dingbot, you can use `easydingbot rm-dingbot` command:
```shell
$ easydingbot rm-dingbot
There are 2 dingbots in config as follow:
  * another
  * default
Please choose one of above to remove ("q" to quit) > another
Removed another from config
```
In addition, you can pass their ids to remove directly:
```
$ easydingbot rm-dingbot another default
Removed another from config
Removed default from config
```

## Usage
Easydingbot's purpose is to make dingbot more easily to use, therefore it has only two concise function for now: `inform` and `feedback`.   
Let's start with the `inform` function. It is the most basic function to send specific message to specific dingbot. `inform` has three arguments of `dingbot_id`, `title` and `text`. You can assign `dingbot_id` to choose one of dingbots to send, `title` and `text` can decide the content you are sending.
```python
>>> from easydingbot import inform

    # to "default" dingbot with default title and text
>>> inform()
    # to "default" dingbot with title of "my inform" and text of "something"
>>> inform(title='my inform', text='something')
    # to "another" dingbot with default title and text
>>> inform(dingbot_id='another')
    # to "another" dingbot with title of "my inform" and text of "something"
>>> inform(dingbot_id='another', title='my inform', text='something')
```
If your configuration is correct, then the messages would be sent to your dingtalk groups.    
After that, let's see the `feedback` decorator. This decorator is design for some long-period manual task's feedback.    
> For example, you run a program with `nohup python ... &`, you estimated this program would run for a long time and got away to do something else. No one can tell you the program's running status before you rechecking its log, in other words, no feedback. Think that you find it crashed at 6 hours ago when you recheck the log, maybe you are going mad. Or you find it already finished at 6 hours ago, you wasted 6 hours for subsequent processing. So you need someone to tell you the program's status regardless of finish or crash, `feedback` can do this.

`feedback` decorator has only two arguments of `dingbot_id` and `title`, you can assign `dingbot_id` to choose which dingbot to send, and assign `title` to identify the task name. While

```python
>>> import time
>>> from easydingbot import feedback

>>> @feedback()
>>> def long_time_succeed():
...     time.sleep(3)
...

>>> long_time_succeed()
```
For this example, it will send 2 messages like:

> **TASK NAME**   
> **TIME** : 2020-11-26T15:07:20.738476   
> **STATUS** : START RUNNING

> **TASK NAME**   
> **TIME** : 2020-11-26T15:07:22.861785+08:00   
> **STATUS**: FINISHED   
> **ELAPSED TIME**: 0:00:02.123238

For a task going to crash.
```python
>>> @feedback(dingbot_id='another', title='ANOTHER TASK')
>>> def long_time_failed():
...     time.sleep(3)
...     1 / 0
...

>>> long_time_failed()
```
It will send 2 messages like:

> **ANOTHER TASK**   
> **TIME** : 2020-11-26T15:07:22.962419   
> **STATUS** : START RUNNING


> **ANOTHER TASK**   
> **TIME** : 2020-11-26T15:07:25.056812+08:00   
> **STATUS**: CRASHED   
> **TRACKBACK**: 
> ```
> Traceback (most recent call last):
>  File "/Users/clarmylee/SNV/LAB/easy-dingbot/easydingbot/main.py", line 116, in wrapper
>    result = function(*args, **kwargs)
>  File "/Users/clarmylee/SNV/LAB/easy-dingbot/tests/test_feedback.py", line 50, in some_task_failed
>    1 / 0
>ZeroDivisionError: division by zero
>```