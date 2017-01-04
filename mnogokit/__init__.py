from time import sleep
import click
import os
import sys
import sh
import ConfigParser
from datetime import datetime
from contextlib import contextmanager


for module in ['mongorestore', 'mongodump', 's3fs', 'fusermount', 'sync']:
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
    DEFAULTS = {
            "bucket": 'my-mongobackups',
            "environment": 'dev',
            "mountpoint": '~/mongobackups',
            "s3fs_options": None
    }

    def __init__(self, config_file):
        config_file = expand_path(config_file)
        config = ConfigParser.SafeConfigParser(self.DEFAULTS)
        config.read(config_file)
        if not config.has_section(CONFIG_SECTION):
            config.add_section(CONFIG_SECTION)
        for setting in self.DEFAULTS:
            setattr(self,
                setting, 
                os.environ.get(setting.upper())
                or config.get(CONFIG_SECTION, setting))
            
        self.mountpoint = expand_path(self.mountpoint)


@contextmanager
def mount_s3(bucket, mountpoint, s3fs_options=""):
    if os.path.ismount(mountpoint):
        print("{0} is already mounted, if mounted with S3FS run `fusermount -u"
                "{0}`".format(mountpoint))
        sys.exit(2)
    s3fs_args = [bucket, mountpoint] 
    if s3fs_options:
        s3fs_args += ["-o", s3fs_options]
    s3fs(s3fs_args)
    try:
        yield mountpoint
    finally:
        sync()
        sleep(20)
        fusermount('-u', mountpoint)

def read_config(environment, config_file):
    config = Config(config_file or DEFAULT_CONFIG_FILE)
    config.environment = environment or config.environment
    if not os.path.exists(config.mountpoint):
        os.makedirs(config.mountpoint)
    return config
