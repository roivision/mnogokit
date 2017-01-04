# Mnogokit

`mnogokit --help`

Backup and restore Mongo DB from and to S3, using `s3fs`, optionally passing a list of collections to iterate over.

## Requirements

- `mongorestore` and `mongodump`
- configure S3FS AWS credentials `echo $AWSACCESSKEYID:$AWSSECRETACCESSKEY > ~/.passwd-s3fs`
- optional `~/.mnogokit` config file, defaults are:
```
[mnogokit]
bucket = gazelle-mongobackups
environment = dev
mountpoint = ~/mongobackups
```
- optional environment variables: `BUCKET` `ENVIRONMENT` `MOUNTPOINT`
- install dependencies `pip install -r requirements.txt && pip install -e .`

## Backup

Run `mnogokit.backup --help`.
Mongo dump options are passed directly to `mongodump`

Examples:
```
mnogokit.backup # backups all the databases
mnogokit.backup -m "commit message" # adds a `COMMIT` file with the message along the dump
mnogokit.backup -d some_db -c c1,c2,c3 # dumps collections `c1` `c2` `c3` from `some_db`
mnogokit.backup -C /etc/my_backup.conf # uses the `/etc/my_backup.conf` configuration file
S3FS_OPTIONS="iam_role=auto,uid=1000" mnogokit.backup # if using IAM role and user ID 1000 to run the command
```

## List backups

`mnogokit.ls [-E env]`

## Import

Use `mnogokit.ls` output path to chose backup to restore.
Run `mnogokit.restore --help`.
Mongo restore options are passed directly to `mongorestore`

Examples:
```
mnogokit.ls -E <environment>
mnogokit.restore <s3 path> # restore data from the `s3 path`
mnogokit.restore -d <database> <s3 path> # restore data from the `s3 path` into specified `database`
mnogokit.restore -d <database> -c <collection> <s3 path to a bson> # restore into specific collection
mnogokit.restore -d <database> --collections c1,c2,c3 <s3 path to a folder containing bsons> # restore bson files in the `s3 path` into their matching collection
```
