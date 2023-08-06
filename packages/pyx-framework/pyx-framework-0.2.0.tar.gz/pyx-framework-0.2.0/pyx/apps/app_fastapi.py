import uvicorn

from os import path
from pathlib import Path
from typing import Optional

from json import loads
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse

from pyx.utils import classproperty
from pyx.utils.id import __PYX_ID__
# you can import any pyx.utils,
# except pyx.utils.app and pyx.utils.dom,
# because it raises ImportError('... (most likely due to a circular import) ...')

make_response = HTMLResponse

__cookies__ = {}
__requests__ = {}

_app: Optional[FastAPI] = None


class HashableRequest(Request):
    def __hash__(self):
        result = []
        for i, k in self.scope.items():
            try:
                if isinstance(k, dict):
                    result.append((i, tuple(k.items())))
                else:
                    result.append((i, tuple(k)))
            except:
                pass
        return hash(tuple(result))


request: Request = HashableRequest({'type': 'http', 'headers': ''})


def _set_request(req):
    global request
    request = req
    request.__class__ = HashableRequest


class SessionError(ConnectionError):
    pass


class RequestError(ConnectionError):
    pass


def _run(*, name, **kwargs):
    kwargs.setdefault('host', '0.0.0.0')
    kwargs.setdefault('reload', True)
    kwargs.setdefault('debug', False)
    kwargs.setdefault('workers', 3)
    return uvicorn.run(name + ':app', **kwargs)


def create_app(name='<pyx>', **kwargs):
    global _app
    _app = FastAPI(name=name, **kwargs)
    _app.run = _run
    _app.mount(
        '/pyx/static',
        StaticFiles(
            directory=path.relpath(
                (Path(path.abspath(__file__)) / '../../static').resolve()
            )
        ),
        name='static',
    )

    @_app.middleware("http")
    async def _setting_request_to_scope(req: Request, call_next):
        _set_request(req)
        return await call_next(req)
    return _app


def get_cookies():
    return request.cookies | __cookies__.get(request, {})


def get_cookie(key, default=None):
    return request.cookies.get(key, default) or __cookies__.get(request, {}).get(key)


def set_cookie(key, value, response: Response = None, **kwargs):
    if response is None:
        if request not in __cookies__:
            __cookies__[request] = {}
        __cookies__[request][key] = value
        return
    response.set_cookie(key=key, value=value, **kwargs)
    if request in __cookies__:
        del __cookies__[request]
    return response


def get_session_id():
    return get_cookie(__PYX_ID__)


def create_request(salt_id, key, value):
    if salt_id not in __requests__:
        __requests__[salt_id] = {}
    __requests__[salt_id][key] = value


def get_request(salt_id, key):
    return __requests__.get(salt_id, {}).get(key)


def _from_request(target, html):
    return dict(target=target, html=str(html))


def handle_requests(request_prefix, on_error, rerender):
    @_app.get(request_prefix + '/{name}')
    @_app.post(request_prefix + '/{name}')
    async def __pyx__requests__(req: Request, name: str):
        _error_status = 500
        kw = dict(req.query_params) | dict(loads(await req.body()))
        try:
            try:
                req = get_request(get_session_id(), name)
            except SessionError:
                raise SessionError(__PYX_ID__)
            if not req:
                _error_status = 400
                raise RequestError('Bad Request')
            _id = kw.pop('id')
            print(req(**kw))
            return _from_request(_id, rerender(_id))
        except Exception as error:
            return JSONResponse(
                _from_request('error', on_error(str(error), kw)), _error_status
            )

    return __pyx__requests__


def __index__(func):
    rules = dict((r.path, r.endpoint) for r in _app.routes if hasattr(r, 'endpoint'))

    if '/' not in rules:
        return _app.get('/')(_app.post('/')(func))
    else:
        print(f'index route exists, using {rules["/"]} endpoint')


class utils:
    _query: dict = {}
    _path: dict = {}
    _host: str = ''

    @classproperty
    def query(cls):
        if not cls._query:
            try:
                cls._query = request.query_params
            except KeyError:
                pass
        return cls._query

    @classproperty
    def path(cls):
        if not cls._path:
            cls._path = request.path_params
        return cls._path

    @classproperty
    def host(cls):
        if not cls._host:
            cls._host = request.client.host
        return cls._host


__all__ = [
    'SessionError',
    'RequestError',
    'create_app',
    'get_cookies',
    'get_cookie',
    'set_cookie',
    'get_session_id',
    'create_request',
    'get_request',
    'handle_requests',
    '__index__',
    'make_response',
    'utils',
]
