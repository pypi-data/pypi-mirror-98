import re

from .default import cached_tag, __extra__
from ..utils import get_random_name


class style(**cached_tag.extend):
    def __init__(self, *, lang='css', scoped=False, head=False, children=''):
        if scoped:
            scoped, children = self._scope_style(children)
        self.lang = lang
        self.head = head
        self.scoped = scoped
        self.children = children

    def _scope_style(self, styles):
        """https://stackoverflow.com/a/32134836/8851903"""
        style_name = get_random_name()
        scoped_data = f'pyx-style="{style_name}"'
        css_rules = re.findall(r'[^{]+{[^}]*}', styles, re.MULTILINE)
        return (
            ('pyx-style', style_name),
            '\n'.join(
                ','.join(
                    f'[{scoped_data}] {item}'
                    for item in rule.strip().split(',')
                )
                for rule in css_rules
            ) + '\n'
        )

    def __render__(self):
        attr, style_name = self.scoped
        self.parent.kw[attr] = style_name
        if self.head:
            __extra__.css += self.children
        else:
            return super().__render__(self.children)
