from .default import DEFAULT_TAG, VOID_TAG
from ..utils.children import ChildType


@DEFAULT_TAG
def a(href=None, *, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def abbr(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def acronym(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def address(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def applet(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def area(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def article(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def aside(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def audio(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def b(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def base(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def basefont(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def bdi(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def bdo(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def big(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def blockquote(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def br(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG.update(is_in_dom=True)
def button(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def canvas(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def caption(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def center(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def cite(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def code(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def col(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def colgroup(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def data(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def datalist(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dd(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG.update(title='del')
def _del(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def details(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dfn(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dialog(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dir(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def div(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dl(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dt(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def em(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def embed(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def fieldset(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def figcaption(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def figure(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def font(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def footer(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def form(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def frame(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def frameset(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h1(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h2(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h3(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h4(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h5(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h6(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def header(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def hr(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def i(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def iframe(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def img(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG.update(title='input')
def _input(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def ins(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def kbd(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def label(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def legend(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def li(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def link(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def main(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG.update(title='map')
def _map(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def mark(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def meta(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def meter(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def nav(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def noframes(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def noscript(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG.update(title='object')
def _object(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def ol(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def optgroup(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def option(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def output(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def p(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def param(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def picture(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def pre(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def progress(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def q(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def rp(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def rt(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def ruby(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def s(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def samp(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def section(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def select(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def small(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def source(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def span(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def strike(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def strong(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def sub(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def summary(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def sup(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def svg(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def table(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def tbody(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def td(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def template(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def textarea(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def tfoot(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def th(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def thead(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def time(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def title(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def tr(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def track(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def tt(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def u(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def ul(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def var(*, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def video(*, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def wbr(*, children: ChildType = '') -> ChildType:
    return children
