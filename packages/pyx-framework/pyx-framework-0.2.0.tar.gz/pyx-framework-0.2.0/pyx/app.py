import os
from pyx import DEFAULT_TAG, render, run_app
from pyx.utils.app import __index__


tags_set = []
__pyx__ = lambda: ''
DEBUG = os.environ.get('DEBUG', False)
__PYX_FILE__ = os.environ.get('__PYX__', '.')
try:
    exec(f'from {__PYX_FILE__} import *')
    exec(f'from {__PYX_FILE__} import __pyx__')
except ImportError as e:
    print(e)

__pyx__ = DEFAULT_TAG.update(title='pyx')(__pyx__)


@__index__
def index():
    return render(__pyx__)


if __name__ == '__main__':
    run_app(name=__PYX_FILE__, debug=DEBUG)
