import os
env = lambda e, d: os.environ[e] if os.environ.has_key(e) else d

DEBUG = bool(env('FLASK_DEBUG', True))

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', None)
