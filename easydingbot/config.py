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
import json
from getpass import getpass


class ConfigNotFound(Exception):
    pass


class TokenError(Exception):
    pass


class URLError(Exception):
    pass


class SecretError(Exception):
    pass


def add_dingbot(dingbot_id=None, *args, **kwargs):
    """Add a dingbot config with interactive input"""
    home = os.path.expanduser('~')
    configfp = os.path.join(home, '.easydingbot')
    if os.path.exists(configfp):
        with open(configfp) as f:
            config_dict = json.load(f)
        if 'default' in config_dict:
            if not dingbot_id:
                dingbot_id = input('Please input the dingbot id ("default" if empty, "q" to quit) > ')
                if dingbot_id.lower() == 'q':
                    exit()  
                if not dingbot_id:
                    dingbot_id = 'default'
        else:
            print('It\'s first time to set dingbot, We will use "default" as the first dingbot id.')
            dingbot_id = 'default'
    else:
        config_dict = {}

    webhook = getpass('Please input the webhook string ("q" to quit) > ')
    if webhook.lower() == 'q':
        exit()  

    secret = getpass('Please input the secret string ("q" to quit) > ')
    if secret.lower() == 'q':
        exit() 

    config_dict[dingbot_id] = {
        'webhook': webhook,
        'secret': secret
    }

    with open(configfp, 'w') as f:
        json.dump(config_dict, f)
        

def list_dingbots(*args, **kwargs):
    """List dingbots in config"""
    home = os.path.expanduser('~')
    configfp = os.path.join(home, '.easydingbot')
    with open(configfp) as f:
        config_dict = json.load(f)

    amount = len(config_dict)
    if amount > 0:
        print(f'There are {len(config_dict)} dingbots in config as follow:')
        for k in sorted(config_dict.keys()):
            print(f'  * {k}')
    else:
        print(f'There are no dingbot in config, please use "easydingbot add-dingbot" command to add one')
        
        
def remove_dingbot(*args, **kwargs):
    """Remove a dingbot config"""
    home = os.path.expanduser('~')
    configfp = os.path.join(home, '.easydingbot')

    with open(configfp) as f:
        config_dict = json.load(f)

    if len(config_dict) > 0:
        args = list(args)
        rm_args = []
        if len(args) > 0:
            for arg in args:
                if arg in config_dict:
                    config_dict.pop(arg)
                    rm_args.append(arg)
                    print(f'Removed {arg} from config')
                    with open(configfp, 'w') as f:
                        json.dump(config_dict, f)
            diffargs = set(args) - set(rm_args)
            if diffargs:
                argstring = ','.join(diffargs)
                print(f'Can\'t remove {argstring} because they are not in config')
        else:
            list_dingbots()
            dingbot_id = input('Please choose one of above to remove ("q" to quit) > ')
            if dingbot_id.lower() == 'q':
                exit()
            if dingbot_id in config_dict:
                config_dict.pop(dingbot_id)
                with open(configfp, 'w') as f:
                    json.dump(config_dict, f)
                print(f'Removed {dingbot_id} from config')
            else:
                raise ConfigNotFound(f'The {dingbot_id} is not in config')


home = os.path.expanduser('~')
configfp = os.path.join(home, '.easydingbot')
if not os.path.exists(configfp):
    print('There be no config file to load, please use "easydingbot add-dingbot" to add one')
else:
    with open(configfp) as f:
        configs = json.load(f)
