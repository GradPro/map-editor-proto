# -*- coding: UTF-8 -*-
from main import app
from views import index, map_edit

# http://flask.pocoo.org/docs/api/#flask.Flask.add_url_rule

# 首頁
app.add_url_rule('/', 'home', index.home)

# 地圖清單
app.add_url_rule('/maps/list', 'map.list', map_edit.map_list)
# 新增地圖
app.add_url_rule('/maps/add', 'map.add', map_edit.map_editor, methods=['GET', 'POST'])
# 編輯地圖
app.add_url_rule('/maps/edit/<int:mid>', 'map.edit', map_edit.map_editor, methods=['GET', 'POST'])
