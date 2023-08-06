# PYX
### A python-based realtime frontend framework

## examples
> ### pages: [first](https://pyx-tests.vercel.app/1), [second](https://pyx-tests.vercel.app/2), [third](https://pyx-tests.vercel.app/3)
> ### composed: [tabs](https://pyx-tests.vercel.app/1)

# use
```python
# tests/test_1.py
from pyx import Tag

@Tag
def name(*, attr):
    return 'Child'

def __pyx__():
    """entrypoint for pyx"""
    return name(attr=1, only_view_attr=True)
```
will render
```html
...
<body>
    <pyx>
        <name attr="1" only_view_attr>
            Child
        </name>
    </pyx>
</body>
...
```
### and
```python
# tests/test_2.py
from pyx import cached_tag, state, button, style, br, div

@cached_tag.update(title='div')
def func(tag):
    tag.count = state(0)
    def increment():
        tag.count += 1
    def decrement():
        tag.count -= 1
    return [
        div(_class='text', children=f'Count: {tag.count}'),
        br(),
        button(_class='button', on_click=increment, children="++"),
        br(),
        button(_class='button', on_click=decrement, children="––"),
        style(scoped=True, children='''
            .text, .button {
                font-size: 1rem;
            }
            .button {
                background: none;
                border: 1px solid red;
                border-radius: .1rem;
            }
        ''')
    ]


# can be simplified as __pyx__ = func
def __pyx__():
    """entrypoint for pyx"""
    return func()

```
will render
```html
...
<body>
    <pyx>
        <div pyx-style="<random style>">
            <div class="text">Count: -5</div>
            <br>
            <button on_click="<fn hash>" class="button">++</button>
            <br>
            <button on_click="<fn hash>" class="button">––</button>
            <style>[pyx-style="<random style>"] .text, [pyx-style="<random style>"] .button {
                font-size: 1rem;
            }
    
            [pyx-style="<random style>"] .button {
                background: none;
                border: 1px solid red;
                border-radius: .1rem;
            }</style>
        </div>
    </pyx>
    <error>
        <render_error></render_error>
        <!-- place for error from request -->
    </error>
    <script>
    
        $('[pyx-id="<tag hash>"]').parent().attr('pyx-style', '<random style>')
    
    </script>

</body>
...
```
## and with parser .pyx
```python
# tests/test_3.pyx
from pyx import Tag, state, select, p  # not necessary, really

@cached_tag.update(title='div')
def func(tag):
    tag.selected = state(1)
    items = {0: 'first', 1: 'second', 2: 'third'}
    def _select(value):
        tag.selected = int(value)
    return <>
        <p>Key: {tag.selected}</p>
        <p @click.right:prevent={lambda: 'GOT IT'}>Value: {items[tag.selected]}</p>
        <select
            items={items}
            @change:prevent={_select}
            value={tag.selected}
        />
    </>


__pyx__ = func
```
will render
```html
...
<body>
    <div>
        <p>Key: 0</p>
        <!-- will be called on contextmenu event with .preventDefault() -->
        <p @click.right:prevent="<fn hash>">Value: first</p>
        <!-- will be called on change event with .preventDefault() -->
        <select @change:prevent="<fn hash>" value="0">
            <option label="first" value="0" selected>first</option>
            <option label="second" value="1">second</option>
            <option label="third" value="2">third</option>
        </select>
    </div>
</body>
...
```
### or merge them with tabs component
```python
# tests/test_tabs.py
from pyx import tabs, tab, style, __APP__ as app
from pyx.utils.app import utils

from tests import test_1, test_2, test_3


def main():
    query = utils.query
    tabs_list = [
        dict(name='page 1', children=test_1.__pyx__, url='/?page=1'),
        dict(name='page 2', children=test_2.__pyx__, url='/?page=2'),
        dict(name='page 3', children=test_3.__pyx__, url='/?page=3')
    ]
    return [
        tabs(
            selected='page ' + query['page'] if 'page' in query else None,
            _class='content',
            children=[tab(**kw) for kw in tabs_list],
        ),
        style(scoped=True, head=True, children='''
            ul {
                list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #f1f1f1;
            }
            
            /* Float the list items side by side */
            tab {
                float: left;
            }
            
            /* Change background color of links on hover */
            tabs tab:hover {
                background-color: #ddd;
            }
            
            /* Create an active/current tablink class */
            tabs tab:focus, tabs tab[active] li {
                background-color: #ccc;
            }
            
            /* Style the links inside the list items */
            li {
                font-family: "Lato", sans-serif;
                display: inline-block;
                color: black;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
                transition: 0.3s;
                font-size: 17px;
            }
            
            /* Style the tab content */
            .content {
                padding: 6px 12px;
                -webkit-animation: fadeEffect 1s;
                animation: fadeEffect 1s;
            }
        '''),
    ]


__pyx__ = main
```
### or you can render all three at once
```python
# tests/app_fastapi.py
from pyx import render, run_app, __APP__

from tests import test_1, test_2, test_3, test_tabs


@__APP__.get('/1')
def test_1_route():
    return render(test_1)


@__APP__.get('/2')
def test_2_route():
    return render(test_2)


@__APP__.get('/3')
def test_3_route():
    return render(test_3)


@__APP__.get('/tabs')
def test_tabs_route():
    return render(test_tabs)


if __name__ == '__main__':
    run_app(name='tests.app_fastapi')
else:
    app = __APP__  # for uvicorn / vercel
```
### `__PYX__=modulename python -m pyx.app`

# install
### now PYX use Flask for render
- `pip install -r requirements.txt`

# .pyx
## File watcher for Intellij Idea family:
### Editor -> File Types -> New -> .pyx
### Settings -> Tools -> File Watchers -> New ->
#### File type: .pyx
#### Program: python
#### Arguments: <project path>/pyx/pyx_parser.py
### #TODO: cli file watcher && other IDE support

