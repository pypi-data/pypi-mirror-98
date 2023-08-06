import re

from ..utils import __extra__
from ..main import cached_tag, Tag


DEFAULT_HEAD = '''
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type="text/javascript" src="/pyx/static/js/pyx.js"></script>
<script type="text/typescript" src="/pyx/static/js/test.ts"></script>
<link type="text/css" rel="stylesheet" href="/pyx/static/css/pyx.css"/>
<style>
    {extra_css}
</style>
{extra_head}
'''

__extra__.css = ''
__extra__.head = ''

DEFAULT_BODY = '''
<error>
    <render_error/>
</error>
<script>
    {extra_js}
</script>
{extra_body}
'''

__extra__.js = ''
__extra__.body = ''

DEFAULT_TAG: Tag = cached_tag.update(is_in_dom=False)
MAIN_TAG: Tag = cached_tag.update(escape=False)
VOID_TAG: Tag = DEFAULT_TAG.update(_void_tag=True)


@Tag
def python(tag: Tag, **k):
    """
    <python>
        # this code will be compiled as a function with current locals
        # and the result of function will be returned to html
        print("Hey, python tag!")
        return 1 + 1
    </python>

    # in console
    Hey, python tag!
    # in browser
    <python>
        2
    </python>
    """
    __locals = {}
    __globals = globals().copy()
    if '_locals' in k:
        __globals.update(tag.kw.pop('_locals'))
    if 'src' in k:
        with open(k['src'], 'r') as src:
            code = '\n'.join('    ' + line for line in src.readlines())
    else:
        children = str(k.get('children', ''))
        tabs = re.search('\n?(?P<spaces> *)', children).group('spaces')
        code = re.sub('^' + tabs, '    ', children, flags=re.MULTILINE)
    exec(
        f'''
def __python__():
{code}
''',
        __globals,
        __locals,
    )
    return __locals['__python__']()


@DEFAULT_TAG
def render_error(traceback: str, **k) -> str:
    children = f'ERROR:\n  traceback: {traceback}\n  kwargs: {k}'
    print(children)
    return children


class __fragment__(**DEFAULT_TAG.extend):
    def __init__(self, *, children=''):
        self.children = children

    def __render__(self):
        return self.children


@MAIN_TAG
def __head__(*, children=''):
    return (
        DEFAULT_HEAD.format(extra_css=__extra__.css, extra_head=__extra__.head,)
        + children
    )


@MAIN_TAG
def __body__(*, children=''):
    return children + DEFAULT_BODY.format(
        extra_js=__extra__.js, extra_body=__extra__.body,
    )


@MAIN_TAG
def __html__(*, head='', children=''):
    __extra__.css = ''
    __extra__.head = ''
    __extra__.js = ''
    __extra__.body = ''
    _body = __body__(children=str(children))
    _head = __head__(children=str(head))
    return [_head, _body]
