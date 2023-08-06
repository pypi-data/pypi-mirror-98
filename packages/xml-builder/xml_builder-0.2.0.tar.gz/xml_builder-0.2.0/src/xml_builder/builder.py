import xml.etree.ElementTree as etree
from typing import Optional, Type, Union, Tuple, Callable
from types import TracebackType


class Node:
    def __init__(self, builder: etree.TreeBuilder):
        self._builder = builder


class Tag(Node):
    def __init__(self, builder: etree.TreeBuilder, name: str, **attrs: str) -> None:
        super().__init__(builder)
        self.name = name
        self.attrs = attrs

    def __enter__(self) -> "Tag":
        self._builder.start(self.name, {k: v for k, v in self.attrs.items()})
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self._builder.end(self.name)


class Text(Node):
    def __init__(self, builder: etree.TreeBuilder, data: str):
        super().__init__(builder)
        self._builder.data(data)


class Builder:
    def __init__(self) -> None:
        self._builder = etree.TreeBuilder()

    def tag(self, name: str, **attrs: str) -> Tag:
        return Tag(self._builder, name, **attrs)

    def text(self, data: str) -> Text:
        return Text(self._builder, data)

    def build(self) -> etree.Element:
        return self._builder.close()
