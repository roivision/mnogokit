from time import sleep
import click
import os
import sys
import sh
import ConfigParser
from datetime import datetime
from contextlib import contextmanager


for module in ['mongodump', 's3fs', 'fusermount', 'sync']:
    try:
        globals()[module] = getattr(sh, module)
    except:
        print("{} is not installed".format(module))
        raise

CONFIG_SECTION = 'mnogokit'
DEFAULT_CONFIG_FILE = '~/.mnogokit'
timestamp = datetime.now().strftime('%Y-%m-%d-%H%M')

def expand_path(path):
    expanded_path = os.path.expanduser(path)
    expanded_path = os.path.expandvars(expanded_path)
    return expanded_path

class Config():
    defaults = {
            "bucket": 'gazelle-mongobackups',
            "environment": 'dev',
            "mountpoint": '~/mongobackups',
    }

    def __init__(config_file):
        config_file = expand_path(config_file)
        config = ConfigParser.SafeConfigParser(defaults)
        config.read(config_file)
        if not config.has_section(CONFIG_SECTION):
            config.add_section(CONFIG_SECTION)
        for setting in defaults:
            setattr(self,
                setting, 
                os.environ.get(setting.upper())
                or config.get(CONFIG_SECTION, setting))
            
        self.mountpoint = expand_path(self.mountpoint)
        if not os.path.exists(config.mountpoint):
            os.makedirs(config.mountpoint)

pass_conf = click.make_pass_decorator(Config)

@contextmanager
def mount_s3(bucket, mountpoint):
    s3fs([bucket, mountpoint])
    yield mountpoint
    sync()
    sleep(10)
    fusermount('-u', mountpoint)
