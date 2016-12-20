import click
import os
from mnogokit import pass_conf, mount_s3
import boto3

@click.command(
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
    ))
@pass_conf
def ls(config):
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects')
    # https://github.com/boto/boto3/blob/develop/boto3/examples/s3.rst#list-top-level-common-prefixes-in-amazon-s3-bucket
    for result in paginator.paginate(
            Bucket=config.bucket,
            Delimiter='/',
            Prefix='{}/'.format(config.environment)):
        for prefix in result.get('CommonPrefixes'):
            prefix_value = prefix.get('Prefix') 
            try:
                commit_msg = client.get_object(
                        Bucket=config.bucket,
                        Key=prefix_value.join('COMMIT'))
            except:
                commit_msg = "No commit message"
            print(': '.join([prefix_value, commit_msg]))


