import click
from mnogokit import Config, DEFAULT_CONFIG_FILE
from mnogokit.backup import backup, restore

@click.group(chain=True)
@click.option('--config-file', '-C', required=False)
@click.pass_context
def cli(ctx, config_file):
    config = Config(config_file or DEFAULT_CONFIG_FILE))
    ctx.obj = config

cli.add_command(backup)
cli.add_command(restore)

if __name__ == '__main__':
    cli()

