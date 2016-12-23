import click
import os
from mnogokit import timestamp, mount_s3, mongodump


@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@click.option('--db', '-d', required=False)
@click.option('--collection', '-c', required=False)
@click.option('--message', '-m', required=False)
@click.pass_context
def backup(ctx, db, collection, message):
    config = ctx.obj
    if db:
        ctx.args[:0] = ['--db', db]
    with mount_s3(config.bucket, config.mountpoint) as mounted:
        destination =  os.path.join(config.mountpoint, config.environment, timestamp)
        if not os.path.exists(destination):
            os.makedirs(destination)
        if collection:
            collection = collection.split(",")
            for col in collection:
                mongodump(
                        "--collection", col,
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
