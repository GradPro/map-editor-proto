# -*- coding: UTF-8 -*-
import os

# 如果環境變數中有e就回傳e的值，不然就回傳d
env = lambda e, d: os.environ[e] if os.environ.has_key(e) else d

DEBUG = bool(env('FLASK_DEBUG', True))

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', None)
