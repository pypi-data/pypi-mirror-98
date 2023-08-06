from .default import DEFAULT_TAG
from ..utils import __extra__


class script(**DEFAULT_TAG.extend):
    def __init__(self, scoped=True, children='', src='', **kwargs):
        self.scoped = scoped
        self.children = children
        self.src = src
        self.kwargs = kwargs

    def __render__(self):
        if not self.scoped:
            __extra__.js += str(self.kw.pop('children'))
            return
        return super().__render__()
