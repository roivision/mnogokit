import click
from mnogokit import pass_conf, timestamp, mount_s3

@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@click.option('--database', '-d', required=False)
@click.option('--collections', '-c', required=False)
@click.option('--message', '-m', required=False)
@pass_conf
def backup(config, database, collections, message):
    with mount_s3(config.bucket, config.mountpoint) as mounted:
        destination =  os.path.join(config.mountpoint, config.environment, timestamp)
        if not os.path.exists(destination):
            os.makedirs(destination)
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
