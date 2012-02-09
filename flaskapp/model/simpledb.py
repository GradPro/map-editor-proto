import boto
from flaskapp import cfg

sdb = boto.connect_sdb(aws_access_key_id=cfg.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=cfg.AWS_SECRET_ACCESS_KEY)
