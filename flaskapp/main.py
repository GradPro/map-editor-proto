# -*- coding: UTF-8 -*-
from flask import Flask
import boto
import cfg

#初始化 Web APP
app = Flask(__name__)

sdb_con = boto.connect_sdb(aws_access_key_id=cfg.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=cfg.AWS_SECRET_ACCESS_KEY)
