from json import dumps, loads
from datetime import date, datetime
from typing import Callable, Optional


def date_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')


def object_hook(obj):
    _isoformat = obj.get('_isoformat')
    if _isoformat is not None:
        return datetime.fromisoformat(_isoformat)
    return obj


def set_data(data, *, serializable=date_serial):
    return dumps(data, default=serializable)


def resolve_data(json_data, *, object_hook: Optional[Callable] = object_hook):
    return loads(json_data, object_hook=object_hook)
