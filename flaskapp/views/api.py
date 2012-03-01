# -*- coding: UTF-8 -*-
from flask import request, abort, jsonify
from flaskapp.model.maps import GameMap

def maps(mid=None):
    if mid:
        map_item = GameMap.get_by_auto_id(mid)
        if map_item:
            if request.method == 'PUT':
                name = request.form.get('name')
                if not name: name = '無標題'
                map_item.name = name
                map_item.grid = request.form.get('grid')
                map_item.save()
                return jsonify(map=map_item.to_dict()['GameMap'])
            elif request.method == 'DELETE':
                map_item.delete()
                return jsonify(map={'id': map_item.id})
            else:
                return jsonify(map=map_item.to_dict()['GameMap'])
        else:
            abort(404)
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            if not name: name = '無標題'
            map_item = GameMap(
                               name=name,
                               width=request.form.get('width', type=int),
                               height=request.form.get('height', type=int),
                               grid=request.form.get('grid')
                               )
            map_item.save()
            return jsonify(map=map_item.to_dict()['GameMap'])
        else:
            all_map = GameMap.query(GameMap.all(), attrs=['mid', 'name', 'width', 'height'], consistent=True)
            all_map = [m.to_dict()['GameMap'] for m in all_map]
            return jsonify(maps=all_map)
