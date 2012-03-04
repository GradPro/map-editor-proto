# -*- coding: UTF-8 -*-
from flask import render_template

def home():
    # 顯示指定樣板
    return render_template('index.html')
