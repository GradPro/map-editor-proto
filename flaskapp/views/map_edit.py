# -*- coding: UTF-8 -*-
from flask import render_template, request, redirect, url_for
from flaskapp.model.maps import GameMap

def map_list():
    maps = GameMap.all()
    return render_template('map_list.html', maps=maps)

def map_editor(mid=None):
    #將map存於SDB
    if request.method == 'POST':
        name = request.form.get('name')
        if not name: name = '無標題'
        grid = request.form.get('grid')
        if mid:
            map_item = GameMap.get_by_id('map_'+str(mid))
            map_item.name = name
            map_item.grid = grid
            map_item.save()
            return redirect(url_for('map.list'))
        else:
            map_item = GameMap(name=name,
                               width=request.form.get('width', type=int),
                               height=request.form.get('height', type=int),
                               grid=grid)
            map_item.save()
            return redirect(url_for('map.list'))
    #從SDB 中取得map
    else:
        if mid:
            map_item = GameMap.get_by_id('map_'+str(mid))
        else:
            map_item = {
                        'width': request.args.get('w', 10, type=int),
                        'height': request.args.get('h', 10, type=int),
                        }
        return render_template('map_editor.html', map=map_item)
