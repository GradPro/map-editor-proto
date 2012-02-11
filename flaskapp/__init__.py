# -*- coding: UTF-8 -*-
from main import app

# 組態設定
import cfg
app.config.from_object(cfg)

# 網址對應 view functions
import urls

# 樣板設定
import tpl
