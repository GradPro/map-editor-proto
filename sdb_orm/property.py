import functools, math, uuid, re
from boto.sdb.db.property import Property, StringProperty
from boto.sdb.db.blob import Blob

def autoID2Attr(i, zeros_to_fill):
    fmt = '%0' + str(zeros_to_fill) + 'u'
    attr = None
    if isinstance(i, int):
        assert math.log10(i) < zeros_to_fill, 'auto id exceeded'
        attr = fmt % i
    return attr if attr else i

def attr2AutoID(a):
    return int(a, 10)

class AutoIDProperty(Property):
    __auto_id_pattern = None
    __bound = None
    __zeros_to_fill = None
    __autoID2Attr = None
    __tmp_obj = None
    __value_to_save = None

    def __init__(self, verbose_name=None, name=None, auto_id_pattern='%(cls)s_%(id)s', bound=10**7):
        Property.__init__(self, verbose_name=verbose_name, name=name, default=None,
                          required=True, validator=None, choices=None, unique=False)
        self.__auto_id_pattern = auto_id_pattern
        self.__bound = bound
        self.__zeros_to_fill = int(math.log10(self.__bound))
        self.__autoID2Attr = functools.partial(autoID2Attr, zeros_to_fill=self.__zeros_to_fill)

    def __property_config__(self, model_class, property_name):
        model_class._auto_id_pattern = self.__auto_id_pattern
        model_class._autoID2Attr = self.__autoID2Attr
        Property.__property_config__(self, model_class, property_name)

    def __get__(self, obj, objtype):
        if obj and obj.id and obj._loaded:
            return attr2AutoID(getattr(obj, self.slot_name))
        else:
            return None

    def __set__(self, obj, value):
        value = self.__autoID2Attr(value)
        if obj is not self.__tmp_obj:
            self.__tmp_obj = obj
            hook = functools.partial(self.__put_hook, obj)
            obj.save = obj.put = hook
        if obj and obj.id and not obj.__dict__.has_key(self.slot_name):
            Property.__set__(self, obj, value)

    def __put_hook(self, obj, expected_value=None):
        self._make_id(obj)
        return self.model_class.put(obj, expected_value=expected_value)

    def _make_id(self, obj):
        if not obj.id:
            obj.id = self.__auto_id_pattern % {'cls': obj.__class__.__name__, 'id': self.get_value_for_datastore(obj)}

    def get_value_for_datastore(self, model_instance):
        if model_instance and model_instance._loaded:
            value = self.__autoID2Attr(getattr(model_instance, self.name))
        else:
            if self.__value_to_save:
                value = self.__value_to_save
                self.__value_to_save = None
            else:
                value = self.__autoID2Attr(self.__query_auto_id())
                self.__value_to_save = value
            Property.__set__(self, model_instance, value)
        return value

    def __query_auto_id(self):
        max_item = None
        for item in self.model_class._manager.domain.select(
                'SELECT %(name)s FROM `%(db)s` WHERE %(name)s IS NOT NULL ORDER BY %(name)s DESC LIMIT 1' %
                {'name': self.name, 'db': self.model_class._manager.db_name}, consistent_read=True, max_items=1):
            max_item = item
        if max_item:
            aid = attr2AutoID(max_item[self.name]) +1
        else:
            aid = 1
        return aid

class BlobProperty(StringProperty):
    __auto_id = None
    __blob = None
    __tmp_obj = None

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('auto_id'):
            self.__auto_id = kwargs['auto_id']
            del kwargs['auto_id']
        StringProperty.__init__(self, *args, **kwargs)

    def __get__(self, obj, objtype):
        if not self.__blob:
            self.__blob = self.model_class._manager.converter.decode_blob(StringProperty.__get__(self, obj, objtype))
        return str(self.__blob)

    def __set__(self, obj, value):
        if obj is not self.__tmp_obj:
            self.__tmp_obj = obj
            hook = functools.partial(self.__put_hook, obj)
            obj.save = obj.put = hook
            hook = functools.partial(self.__delete_hook, obj)
            obj.delete = hook
        self.__blob = self.model_class._manager.converter.decode_blob(value)
        if not self.__blob:
            if obj.__dict__.has_key(self.slot_name):
                self.__blob = self.model_class._manager.converter.decode_blob(StringProperty.__get__(self, obj, None))
            else:
                self.__blob = Blob(value=value)

    def __put_hook(self, obj, expected_value=None):
        bucket = self.model_class._manager.get_blob_bucket()
        if not self.__blob.id:
            if self.__auto_id:
                if not obj.id:
                    self.__auto_id._make_id(obj)
                key = bucket.new_key('%s.%s' % (obj.id, self.name))
            else:
                key = bucket.new_key(str(uuid.uuid4()))
            self.__blob.id = "s3://%s/%s" % (bucket.name, key.name)
        else:
            match = re.match("^s3:\/\/([^\/]*)\/(.*)$", self.__blob.id)
            assert match, "Invalid Blob ID: %s" % self.__blob.id
            key = bucket.get_key(match.group(2))
        key.set_contents_from_string(self.__blob.value)#?
        StringProperty.__set__(self, obj, self.__blob.id)
        return self.model_class.put(obj, expected_value=expected_value)

    def __delete_hook(self, obj):
        try:
            self.__blob.file.delete()
        except AttributeError:
            self.__blob = self.model_class._manager.converter.decode_blob(StringProperty.__get__(self, obj, None))
            self.__blob.file.delete()
        self.model_class.delete(obj)

    def get_value_for_datastore(self, model_instance):
        return getattr(model_instance, self.slot_name)
