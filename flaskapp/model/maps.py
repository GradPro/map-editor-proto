from boto.sdb.db.property import IntegerProperty, StringProperty
from flaskapp.model import AutoIdIncrementExpando

class GameMap(AutoIdIncrementExpando):
    _db_name = 'game-maps'
    __consistent__ = True
    __AutoIdPattern__ = 'map_{incr}'
    __AutoIdAttr__ = 'mid'

    name = StringProperty(required=True)
    width = IntegerProperty(default=None, required=True, min=1)
    height = IntegerProperty(default=None, required=True, min=1)
    grid_part = IntegerProperty(default=None, required=True, min=1)
    _grid_json = ''

    def _get_grid(self):
        if not self._grid_json:
            try:
                for part in xrange(self.grid_part):
                    self._grid_json += self.__getattr__('grid_'+str(part+1))
            except AttributeError:
                pass
        return self._grid_json
    def _set_grid(self, value):
        self._grid_json = value
        self.grid_part = 1 if len(value) < 1000 else (len(value)//1000)
        for part in xrange(self.grid_part):
            self._cache['grid_'+ str(part+1)] = value[part*1000:(part+1)*1000]
    grid = property(_get_grid, _set_grid)

    def __getattr__(self, name):
        if name == 'grid':
            return self._get_grid()
        else:
            return AutoIdIncrementExpando.__getattr__(self, name)
    def __setattr__(self, name, value):
        if name == 'grid':
            self._set_grid(value)
        else:
            AutoIdIncrementExpando.__setattr__(self, name, value)
