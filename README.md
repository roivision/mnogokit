# Mnogokit
## Requirements
- configure S3FS AWS credentials `echo $AWSACCESSKEYID:$AWSSECRETACCESSKEY > ~/.passwd-s3fs`
- optional `~/.mnogokit` config file, defaults are:
```
[mnogokit]
bucket = gazelle-mongobackups
environment = dev
mountpoint = ~/mongobackups
```
- optional environment variables: `BUCKET` `ENVIRONMENT` `MOUNTPOINT`

## Backup

Run `mnogokit.backup`.
Mongo dump options are passed directly to `mongodump`

Examples:
```
mnogokit.backup # backups all the databases
mnogokit.backup -m "commit message" # adds a `COMMIT` file with the message along the dump
mnogokit.backup -d some_db -c c1,c2,c3 # dumps collections `c1` `c2` `c3` from `some_db`
mnogokit.backup -C /etc/my_backup.conf # uses the `/etc/my_backup.conf` configuration file
```

# Import
