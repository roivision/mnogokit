import click
import os
from mnogokit import Config, DEFAULT_CONFIG_FILE
from mnogokit.backup import backup
from mnogokit.restore import restore
from mnogokit.ls import ls

@click.group(chain=True)
@click.option('--environment', '-E', required=False)
@click.option('--config-file', '-C', required=False)
@click.pass_context
def cli(ctx, environment, config_file):
    config = Config(config_file or DEFAULT_CONFIG_FILE)
    config.environment = environment or config.environment
    if not os.path.exists(config.mountpoint):
        os.makedirs(config.mountpoint)
    ctx.obj = config

cli.add_command(backup)
cli.add_command(restore)
cli.add_command(ls)

if __name__ == '__main__':
    cli()

