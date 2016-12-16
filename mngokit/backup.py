import click
from sh import mongodump, s3fs, fusermount


@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@click.option('--collections', '-c', required=False)
@click.option('--destination', '-o', default="/tmp/")
@click.option('--message', '-m', required=False)
@click.pass_context
def parse(ctx, collections, destination, message):
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

def mount(bucket, mountpoint):
    s3fs(bucket, mountpoint)

def umount(mountpoint):
    fusermount('-u', mountpoint)


if __name__ == '__main__':
    print("""install s3fs: apt-get install s3fs""")
    print("""configure s3fs password echo MYIDENTITY:MYCREDENTIAL >
    /etc/passwd-s3fs
    chmod 600 /etc/passwd-s3fs""")
    parse()

