import click
import os
from mnogokit import mount_s3, mongorestore

@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@click.option('--collections', required=False)
@click.option('--config-file', '-C', required=False)
@click.argument('mongo_restore_args', nargs=-1, type=click.UNPROCESSED)
@click.argument('restore_path', required=True)
@click.pass_context
def restore(ctx, collections, config_file, mongo_restore_args, restore_path):
    config = ctx.obj
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

