from time import sleep
import click
import os
import sys
import sh
from datetime import datetime


for module in ['mongodump', 's3fs', 'fusermount', 'sync']:
    try:
        globals()[module] = getattr(sh, module)
    except:
        print("{} is not installed".format(module))
        raise

bucket = 'gazelle-mongobackups'
environment = 'dev'
mountpoint = '~/mongobackups'
timestamp = datetime.now().strftime('%Y-%m-%d %H%M')

def read_config():
    # open config file
    # get variables or ENV.get(x, default)
    pass


@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@click.option('--collections', '-c', required=False)
@click.option('--message', '-m', required=False)
@click.pass_context
def run(ctx, collections, message):
    expanded_mountpoint = os.path.expanduser(mountpoint)
    expanded_mountpoint = os.path.expandvars(expanded_mountpoint)
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
                        "-o", destination,
                        *ctx.args)
            return
        else:
            mongodump(
                    "-o", destination,
                    *ctx.args)
            return
    finally:
        sync()
        sleep(10)
        fusermount('-u', expanded_mountpoint)


if __name__ == '__main__':
    run()

