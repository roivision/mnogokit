from time import sleep
import click
import os
import sys
import sh
import ConfigParser
from datetime import datetime


for module in ['mongodump', 's3fs', 'fusermount', 'sync']:
    try:
        globals()[module] = getattr(sh, module)
    except:
        print("{} is not installed".format(module))
        raise

config_section = 'mnogokit'
defaults = {
    "bucket": 'gazelle-mongobackups',
    "environment": 'dev',
    "mountpoint": '~/mongobackups',
    "config_path": '~/.mnogokit',
    "timestamp": datetime.now().strftime('%Y-%m-%d-%H%M')
}

def read_config(config_file):
    config_file = expand_path(config_file)
    config = ConfigParser.SafeConfigParser(defaults)
    config.read(config_file)
    if not config.has_section(config_section):
        config.add_section(config_section)
    for setting in defaults:
        config.set(
                config_section,
                setting, 
                os.environ.get(setting.upper())
                or config.get(config_section, setting))
    return config

def expand_path(path):
    expanded_path = os.path.expanduser(path)
    expanded_path = os.path.expandvars(expanded_path)
    return expanded_path


@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@click.option('--collections', '-c', required=False)
@click.option('--message', '-m', required=False)
@click.option('--config-file', '-C', required=False)
@click.pass_context
def run(ctx, collections, message, config_file):

    config = read_config(config_file or defaults.get('config_path'))
    bucket = config.get(config_section, 'bucket')
    environment = config.get(config_section, 'environment')
    mountpoint = config.get(config_section, 'mountpoint')
    timestamp = config.get(config_section, 'timestamp')

    expanded_mountpoint = expand_path(mountpoint)
    if not os.path.exists(expanded_mountpoint):
        os.makedirs(expanded_mountpoint)
    try:
        s3fs([bucket, expanded_mountpoint])
    except:
        print("""configure s3fs password echo MYIDENTITY:MYCREDENTIAL >
        /etc/passwd-s3fs
        chmod 600 /etc/passwd-s3fs""")
        raise
    destination =  os.path.join(expanded_mountpoint, environment, timestamp)
    if not os.path.exists(destination):
        os.makedirs(destination)
    try:
        if collections:
            collections = collections.split(",")
            for collection in collections:
                mongodump(
                        "--collection", collection,
                        "-o", '"{}"'.format(destination),
                        *ctx.args)
        else:
            mongodump(
                    "-o", '"{}"'.format(destination),
                    *ctx.args)
        if message:
            commit_file = os.path.join(destination, 'COMMIT')
            with open(commit_file, 'wb') as f:
                f.write(message)
    finally:
        sync()
        sleep(10)
        fusermount('-u', expanded_mountpoint)


if __name__ == '__main__':
    run()

