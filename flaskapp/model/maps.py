from boto.sdb.db.property import StringProperty, IntegerProperty
from sdb_orm.model import Model
from sdb_orm.property import AutoIDProperty, BlobProperty

class GameMap(Model):
    _db_name = 'game-maps'
    __consistent__ = True

    mid = AutoIDProperty(bound=10**8)
    name = StringProperty(required=True)
    width = IntegerProperty(default=None, required=True, min=1)
    height = IntegerProperty(default=None, required=True, min=1)
    grid = BlobProperty(required=True, auto_id=mid)
