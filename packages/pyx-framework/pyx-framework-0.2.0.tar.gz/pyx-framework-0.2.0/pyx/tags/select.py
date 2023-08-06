from typing import Union

from ..utils import JSON
from ..main import cached_tag, Component


class SelectItem(JSON[Union['label', 'value'], object]):
    label: str
    value: str


class SelectItems:
    def __new__(cls, *args, **kwargs) -> list[SelectItem]:
        if (data := kwargs) or (
            len(args) == 1 and (
                isinstance(data := args[0], dict) or (
                    hasattr(args[0], '__get__') and
                    isinstance(data := args[0].__get__(), dict)
                )
            )
        ):
            if 'label' not in data or 'value' not in data:
                return [SelectItem(label=v, value=k) for k, v in data.items()]
            return list(map(SelectItem, data))
        if args:
            return list(map(SelectItem, args))
        return [SelectItem(*args, **kwargs)]


@cached_tag
def option(*, label, **attrs):
    return label


@cached_tag
def select(tag: Component, **k):
    items = SelectItems(tag.kw.pop('items'))
    return [
        option(
            **item,
            selected=(
                tag.kw.value == item.value or
                tag.kw.value == item.label
            )
        )
        for item in items
    ]