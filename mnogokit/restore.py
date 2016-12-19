import click
from mnogokit import pass_conf

@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@click.option('--collections', '-c', required=False)
@click.option('--message', '-m', required=False)
@click.option('--config-file', '-C', required=False)
@click.pass_context
def restore(ctx, collections, message, config_file):
    pass

