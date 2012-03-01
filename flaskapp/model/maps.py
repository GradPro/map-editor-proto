# -*- coding: UTF-8 -*-
from boto.sdb.db.property import StringProperty, IntegerProperty
from sdb_orm.model import Model
from sdb_orm.property import AutoIDProperty, BlobProperty

# 宣告遊戲地圖資料模型
class GameMap(Model):
    # 資料表名稱
    _db_name = 'game-maps'
    # 預設使用一致性讀取，不然有可能會讀到不是最新的資料，因為sdb是分散式資料庫
    __consistent__ = True

    # 自動流水號，此欄位不可設定，只會自動撈資料表中最大值+1
    # bound是流水號可能值的上限，只可以小於它，這邊設為10的8次方
    mid = AutoIDProperty(bound=10**8)
    name = StringProperty(required=True) # 地圖名稱，字串欄位，必要值
    width = IntegerProperty(default=None, required=True, min=1) # 寬，整數欄位
    height = IntegerProperty(default=None, required=True, min=1)
    # 因sdb有欄位值長度不可超過1024的限制，這邊把資料存到Amazon s3變成一個檔案
    # 然後在sdb的欄位裡存路徑，這個屬性經過包裝，可以當字串直接讀寫
    # 傳入auto_id作為自動產生檔名的依據
    grid = BlobProperty(required=True, auto_id=mid)
