from boto import config
from boto.sdb.db.model import Model, Expando
from boto.sdb.db.property import IntegerProperty
from flaskapp import app

config.add_section('DB')
config.set('DB', 'db_user', app.config['AWS_ACCESS_KEY_ID'])
config.set('DB', 'db_passwd', app.config['AWS_SECRET_ACCESS_KEY'])
config.setbool('DB', 'enable_ssl', True)

class AutoIdIncrementModel(Model):
    __AutoIdPattern__ = '{incr}'
    __AutoIdAttr__ = ''
    auto_id = IntegerProperty(default=None, required=True, unique=True, min=1)

    def _query_auto_id(self):
        max_item = None
        for item in self._manager.domain.select(
                'select auto_id from `%s` where auto_id is not null order by auto_id desc' %
                self._db_name, consistent_read=True, max_items=1):
            max_item = item
        if max_item:
            return int(max_item['auto_id']) -2147483648 +1
        else:
            return 1

    def put(self, expected_value=None):
        if not self.auto_id:
            self.auto_id = self._query_auto_id()
        if not self.id:
            self.id = self.__class__.__AutoIdPattern__.format(incr=self.auto_id)
        return Model.put(self, expected_value=expected_value)

    save = put

    def put_attributes(self, attrs):
        if not self.auto_id:
            self.auto_id = self._query_auto_id()
        if not self.id:
            self.id = self.__class__.__AutoIdPattern__.format(incr=self.auto_id)
        return Model.put_attributes(self, attrs)

    def __getattr__(self, name):
        if name == self.__AutoIdAttr__:
            return self.auto_id
        return Model.__getattr__(self, name)


class AutoIdIncrementExpando(Expando):
    __AutoIdPattern__ = '{incr}'
    __AutoIdAttr__ = ''
    auto_id = IntegerProperty(default=None, required=True, unique=True, min=1)
    _cache = {}

    def _query_auto_id(self):
        max_item = None
        for item in self._manager.domain.select(
                'select auto_id from `%s` where auto_id is not null order by auto_id desc' %
                self._db_name, consistent_read=True, max_items=1):
            max_item = item
        if max_item:
            return int(max_item['auto_id']) -2147483648 +1
        else:
            return 1

    def put(self, expected_value=None):
        try:
            self.auto_id
        except AttributeError:
            self.auto_id = self._query_auto_id()
        if not self.id:
            self.id = self.__class__.__AutoIdPattern__.format(incr=self.auto_id)
        for name, value in self._cache.items():
            self.__setattr__(name, value)
        return Expando.put(self, expected_value=expected_value)

    save = put

    def put_attributes(self, attrs):
        try:
            self.auto_id
        except AttributeError:
            self.auto_id = self._query_auto_id()
        if not self.id:
            self.id = self.__class__.__AutoIdPattern__.format(incr=self.auto_id)
        return Expando.put_attributes(self, attrs)

    def __getattr__(self, name):
        if name == self.__AutoIdAttr__:
            return self.auto_id
        return Expando.__getattr__(self, name)

    def __setattr__(self, name, value):
        if not (name in self._prop_names or name.startswith('_') or name == 'id'):
            try:
                self.auto_id
            except AttributeError:
                self.auto_id = self._query_auto_id()
            if not self.id:
                self.id = self.__class__.__AutoIdPattern__.format(incr=self.auto_id)
        Expando.__setattr__(self, name, value)
