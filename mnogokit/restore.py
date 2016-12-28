import click
import os
from mnogokit import mount_s3, mongorestore, read_config

@click.command(context_settings=dict(
        ignore_unknown_options=True,
        ))
@click.option('--environment', '-E', required=False)
@click.option('--config-file', '-C', required=False)
@click.option('--collections', required=False)
@click.argument('mongo_restore_args', nargs=-1, type=click.UNPROCESSED)
@click.argument('restore_path', required=True)
def restore(
        environment,
        config_file,
        collections,
        mongo_restore_args,
        restore_path):
    config = read_config(environment, config_file)
    restore_path =  os.path.join(config.mountpoint, restore_path)
    mongo_restore_args = mongo_restore_args + (restore_path, )
    with mount_s3(config.bucket, config.mountpoint) as mounted:
        if collections:
            collections = collections.split(",")
            for collection in collections:
                mongorestore(
                        "--collection", collection,
                        *list(mongo_restore_args))
        else:
            mongorestore(
                    *list(mongo_restore_args))

