# -*- coding: UTF-8 -*-
from main import app

# 組態設定
import cfg
app.config.from_object(cfg)

# Control function
import index

