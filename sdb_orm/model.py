from boto.sdb.db import model

class Model(model.Model):
    @classmethod
    def _get_by_auto_id(cls, auto_id, manager=None):
        if not manager:
            manager = cls._manager
        obj_id = cls._auto_id_pattern % {'cls': cls.__name__, 'id': cls._autoID2Attr(auto_id)}
        return manager.get_object(cls, obj_id)

    @classmethod
    def get_by_auto_id(cls, auto_ids=None, parent=None):
        if isinstance(auto_ids, list):
            objs = [cls._get_by_auto_id(auto_id) for auto_id in auto_ids]
            return objs
        else:
            return cls._get_by_auto_id(auto_ids)

    get_by_auto_ids = get_by_auto_id

    @classmethod
    def query(cls, query, attrs=[], consistent=False):
        manager = cls._manager
        assert isinstance(attrs, list), 'attrs must be a list'
        attrs = '*' if len(attrs)==0 else ', '.join(attrs + ['__type__','__module__','__lineage__'])
        query_str = 'SELECT %s FROM `%s` %s' % \
            (attrs, manager.domain.name,
             manager._build_filter_part(query.model_class, query.filters, query.sort_by, query.select))
        if query.limit:
            query_str += ' LIMIT %s' % query.limit
        rs = manager.domain.select(query_str, max_items=query.limit, next_token = query.next_token, consistent_read=consistent)
        query.rs = rs
        return manager._object_lister(query.model_class, rs)

class Expando(model.Expando, Model):
    pass
