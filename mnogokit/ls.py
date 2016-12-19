import click
import os
from mnogokit import pass_conf, mount_s3

@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@pass_conf
def ls(config):
    with mount_s3(config.bucket, config.mountpoint) as mounted:
        env_dir = os.path.join(mounted, config.environment)
        print(os.listdir(env_dir))


