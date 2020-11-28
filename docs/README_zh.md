[English Documentation](./README_en.md)

# easydingbot
[![Build Status](https://travis-ci.org/seniverse/easydingbot.svg?branch=main)](https://travis-ci.org/seniverse/easydingbot)
[![PyPI version](https://badge.fury.io/py/easydingbot.svg)](https://badge.fury.io/py/easydingbot)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/seniverse/easydingbot/issues)

Easydingbot 是一个让钉钉机器人更好用的包。

## 安装
你可以用 `pip` 来安装easydingbot
```shell
$ pip install easydingbot
```
或者
```
$ pip install git+https://github.com/seniverse/easydingbot@main
```
## 配置  
在使用easydingbot之前，你需要将你的 **webhook** 和 **secret-code**（秘钥）注入到配置中，请查阅[钉钉机器人文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq) 来了解如何获取webhook和秘钥。   
完成之后，你可以使用 `easydingbot add-dingbot` 命令把它们注入配置：
```shell
$ easydingbot add-dingbot
It's first time to set dingbot, we will use "default" as the first dingbot id.
Please input the webhook string ("q" to quit) >
Please input the secret string ("q" to quit) > 
```
然后你就可以使用 `easydingbot ls-dingbot` 来查看已经注入配置的钉钉机器人的ID：
```shell
$ easydingbot ls-dingbot
There are 1 dingbots in config as follow:
  * default
```
如果你想检查这个配置是否有效，可以使用 `easydingbot touch` 命令来进行一次校验：
```
$ easydingbot touch
Dingbot of default's status is normal.
```
上面的命令等效于 `easydingbot touch default`。  
如果你想要增加另一条机器人配置，你可以给 `easydingbot add-dingbot` 传入新机器人的ID然后进行配置：
```shell
$ easydingbot add-dingbot another
Please input the webhook string ("q" to quit) >
Please input the secret string ("q" to quit) > 
```
之后你的配置中就有了两个机器人。
```
$ easydingbot ls-dingbot
There are 2 dingbots in config as follow:
  * another
  * default
```
你可以通过指定它们的ID去进行touch校验。
```
$ easydingbot touch another
Dingbot of another status is normal.
```
如果你校验的结果显示异常，你怀疑是你输入的webhook或者秘钥不对，你可以再次使用 `easydingbot add-dingbot` 命令，输入相同的机器人ID去覆盖这条配置。   
如果你想要删除一条机器人，你可以使用 `easydingbot rm-dingbot` 命令：
```shell
$ easydingbot rm-dingbot
There are 2 dingbots in config as follow:
  * another
  * default
Please choose one of above to remove ("q" to quit) > another
Removed another from config
```
此外，你也可以传入它们的ID直接删除：
```
$ easydingbot rm-dingbot another default
Removed another from config
Removed default from config
```

## 使用
easydingbot的目的是使钉钉机器人使用起来更简单，因此目前只有两个简介的功能：`inform` 和 `feedback`。   
我们先来看看 `inform` ，这是最基本的功能，它用于向指定的钉钉机器人发送指定的消息。`inform` 有3个参数：`dingbot_id`, `title` 和 `text`。你可以通过 `dingbot_id` 参数去控制要往哪个机器人里面发送消息，用`title` 和 `text` 去控制发送的内容。
```python
>>> from easydingbot import inform

    # 向"default"机器人（默认机器人）发送默认的title和text
>>> inform()
    # 向"default"机器人（默认机器人）发送title为"my inform"， text为"something"的消息
>>> inform(title='my inform', text='something')
    # 向"another"机器人发送默认的title和text
>>> inform(dingbot_id='another')
    # 向"another"机器人发送title为"my inform"， text为"something"的消息
>>> inform(dingbot_id='another', title='my inform', text='something')
```
如果你的配置正确，那么消息应该就已经发送到你的钉钉群里了。   
现在我们再来看看 `feedback` 装饰器，这个装饰器的设计是为了对一些长时间运行的临时性任务的运行状态进行反馈。   

> 举个例子，假如你在后台跑了一个类似于 `nohup python ... &` 的程序，你预计该程序要跑很久，然后你就去做别的事了。在你回来检查日志之前，没有人会告诉你程序的运行状态，也就是说没有反馈机制。试想一下当你检查日志的时候发现程序早在6个小时之前就崩溃了，你是不是也崩溃了？或者你发现它在6个小时之前就已经完成了，这样你有浪费了6个小时时间去进行后续的处理。所以你需要有人去告诉你程序的运行状态：完成了或是崩溃了。 `feedback` 就可以做这个事。

`feedback` 有两个参数：`dingbot_id` 和 `title`，你可以用 `dingbot_id` 来指定要发的机器人，用 `title` 去识别任务的ID。
```python
>>> import time
>>> from easydingbot import feedback

>>> @feedback()
... def long_time_succeed():
...     time.sleep(3)
...

>>> long_time_succeed()
('{"errcode":0,"errmsg":"ok"}', '{"errcode":0,"errmsg":"ok"}')
```
在上面这个例子里，它会发送2条像下面这样的消息：

> **TASK NAME**   
> **TIME** : 2020-11-26T15:07:20.738476+08:00   
> **STATUS** : START RUNNING

> **TASK NAME**   
> **TIME** : 2020-11-26T15:07:22.861785+08:00   
> **STATUS**: FINISHED   
> **ELAPSED TIME**: 0:00:02.123238

`long_time_succeed` 函数的返回值会被 `feedback` 修改为消息状态信息， `('{"errcode":0,"errmsg":"ok"}', '{"errcode":0,"errmsg":"ok"}')` 意味着两条信息都已经发送到钉钉的服务器了，由于这种修改返回值的特性，所以你不应该在任何返回值很重要的函数上使用 `feedback` 装饰器。   
对于会崩溃的任务的例子：
```python
>>> @feedback(dingbot_id='another', title='ANOTHER TASK')
... def long_time_failed():
...     time.sleep(3)
...     1 / 0
...

>>> long_time_failed()
('{"errcode":0,"errmsg":"ok"}', '{"errcode":0,"errmsg":"ok"}', 'ZeroDivisionError: division by zero')
```
对于崩溃的任务，它会在返回值中加一个错误类型。   
它会发送两条类似下面的消息：

> **ANOTHER TASK**   
> **TIME** : 2020-11-26T15:07:22.962419+08:00   
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

此外，你也可以传入自定义的参数，它也会显示在最终的消息内容中，例如：
```python
>>> @feedback(title='CUSTOM', AUTHOR='CLARMY', PRIORITY=5)
... def long_time_succeed():
...     print('long time')
... 
>>> long_time_succeed()
long time
('{"errcode":0,"errmsg":"ok"}', '{"errcode":0,"errmsg":"ok"}')
```
结果:
> **CUSTOM**   
> **AUTHOR**: CLARMY   
> **PRIORITY**: 5   
> **TIME**: 2020-11-28T03:18:49.143275+08:00   
> **STATUS**: START RUNNING

> **CUSTOM**   
> **AUTHOR**: CLARMY   
> **PRIORITY**: 5   
> **TIME**: 2020-11-28T03:18:49.293935+08:00   
> **STATUS**: FINISHED   
> **ELAPSED TIME**: 0:00:00.150647