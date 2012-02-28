# -*- coding: UTF-8 -*-
from flask import render_template, request, redirect, url_for
from flaskapp.model.maps import GameMap

def map_list():
    # 查詢所有的資料，只select指定的欄位，而且使用一致性讀取
    maps = GameMap.query(GameMap.all(), attrs=['mid', 'name', 'width', 'height'], consistent=True)
    return render_template('map_list.html', maps=maps)

def map_editor(mid=None):
    # 將地圖存於sdb，因為連線是POST，瀏覽器上傳資料
    if request.method == 'POST':
        # 從POST參數讀進來
        name = request.form.get('name')
        if not name: name = '無標題'
        grid = request.form.get('grid')
        # 編輯地圖
        if mid:
            map_item = GameMap.get_by_auto_id(mid)
            map_item.name = name
            map_item.grid = grid
            map_item.save()
            return redirect(url_for('map.list'))
        # 新增地圖
        else:
            map_item = GameMap(name=name,
                               width=request.form.get('width', type=int),
                               height=request.form.get('height', type=int),
                               grid=grid)
            map_item.save()
            return redirect(url_for('map.list'))
    #從sdb中取得地圖
    else:
        # 讀取地圖
        if mid:
            map_item = GameMap.get_by_auto_id(mid)
        # 新增地圖
        else:
            # 指定寬高，從網址的參數讀進來，轉成整數型態，預設為10
            map_item = {
                        'width': request.args.get('w', 10, type=int),
                        'height': request.args.get('h', 10, type=int),
                        }
        return render_template('map_editor.html', map=map_item)
