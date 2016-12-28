import click
import os
from mnogokit import mount_s3, read_config
import boto3
from botocore.exceptions import ClientError

@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@click.option('--environment', '-E', required=False)
@click.option('--config-file', '-C', required=False)
@click.pass_context
def ls(ctx, environment, config_file):
    config = read_config(environment, config_file)
    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    bucket = s3.Bucket(config.bucket)
    prev = ""
    for idx, obj in enumerate(bucket.objects.filter(Prefix=config.environment)):
        if obj.key.endswith('COMMIT'):
            continue
        msg = [str(idx), obj.key]
        path_levels = len(obj.key.split('/'))
        if obj.key.endswith('/') and path_levels == 3:
            try:
                commit_msg = client.get_object(
                        Bucket=config.bucket,
                        Key=obj.key + 'COMMIT').get('Body').read()
            except ClientError as e:
                commit_msg = 'no commit message'
            msg.append(commit_msg)
        print(': '.join(msg))



