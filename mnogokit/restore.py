import click
from mnogokit import mount_s3

@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@click.option('--database', required=False)
@click.option('--collections', required=False)
@click.option('--config-file', '-C', required=False)
@click.pass_context
def restore(ctx, database, collections, config_file):
    config = ctx.obj
    if database:
        ctx.args[:0] = ['--database', database]
    with mount_s3(config.bucket, config.mountpoint) as mounted:
        if collections:
            collections = collections.split(",")
            for collection in collections:
                mongodump(
                        "--collection", collection,
                        *ctx.args)
        else:
            mongodump(
                    *ctx.args)

