from .app import get_session_id, SessionError

__sessions__ = {}


def get_dom():
    dom = __sessions__.get(get_session_id())
    if dom is None:
        raise SessionError('cannot get session')
    return dom


def set_dom(_id, dom=None):
    __sessions__[_id] = dom or {}


def del_dom(_id=None):
    _id = _id or get_session_id()
    if _id in __sessions__:
        del __sessions__[_id]


def get_from_dom(tag):
    if isinstance(tag, str):
        _id = tag
    else:
        _id = str(hash(tag))
    return get_dom().get(_id)


def set_to_dom(key_or_value, value=None):
    dom = get_dom()
    if value:
        dom[str(key_or_value)] = value
    else:
        dom[str(hash(key_or_value))] = key_or_value
