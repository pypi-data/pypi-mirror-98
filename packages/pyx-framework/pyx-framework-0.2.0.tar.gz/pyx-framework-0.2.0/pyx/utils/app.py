import os
from typing import Optional, Callable, TypeVar

Response = TypeVar('Response')
APP = TypeVar('APP')

__APP__ = os.environ.get('__APP__', 'FastAPI')


class SessionError(ConnectionError):
    pass


class RequestError(ConnectionError):
    pass


class Route(Callable):
    pass


TAG = Callable[..., str]
SALT_ID = str


create_app: Callable[[str], APP]
get_cookies: Callable[[], Optional[dict[str, str]]]
get_cookie: Callable[[str, Optional[str]], str]
set_cookie: Callable[[str, str, Optional[Response]], Response]
create_request: Callable[[SALT_ID, str, TAG], None]
get_request: Callable[[SALT_ID, str], Optional[TAG]]
handle_requests: Callable[
    [str, Callable[[str, dict], str], Callable[[str], str]], Route[..., Response]
]
__index__: Callable[[Route], None]

make_response: Callable[[str], Response]


class utils:
    query: dict[str, str]
    path: dict[str, str]
    host: str

if __APP__ == 'Flask':
    from pyx.apps.app_flask import *
elif __APP__ == 'FastAPI':
    from pyx.apps.app_fastapi import *
else:
    try:
        exec(f'from {__APP__} import *')
    except ImportError:
        raise ImportError('Cannot find renderer app')


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
