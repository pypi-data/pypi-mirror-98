from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional, Union, cast

from .const import HIGHLIGHT_LANGUAGES

Attr = Dict[str, Optional[str]]


class Content:
    def __init__(self, data: str) -> None:
        self.data = data

    def to_str(self) -> str:
        return self.data


class Tag(metaclass=ABCMeta):
    def __init__(self, name: str, attrs: Attr) -> None:
        self.name = name
        self.attrs = attrs
        self.data = ""
        self.children: List[Element] = []

    def attr(self, attr_name: str) -> str:
        attr_value = self.attrs.get(attr_name, "")
        return cast(str, attr_value)

    def append_child(self, child: Element) -> None:
        self.children.append(child)

    def inner(self) -> str:
        return "".join(child.to_str() for child in self.children)

    def to_str(self) -> str:
        return self.inner()


Element = Union[Content, Tag]

# <html>
class HTML(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("html", attrs)


# <a>
class A(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("a", attrs)

    def to_str(self) -> str:
        ref = self.attr("href")
        return f"[{self.inner()}]({ref})"


# <b>
class B(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("b", attrs)

    def to_str(self) -> str:
        return f"**{self.inner()}**"


# <br>
class Br(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("br", attrs)

    def to_str(self) -> str:
        return "\n"


# <blockquote>
class Blockquote(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("blockquote", attrs)

    def to_str(self) -> str:
        lines = []
        for idx, child in enumerate(self.children):
            child_inner = child.to_str()
            if idx == len(self.children) - 1:
                child_inner = child_inner.rstrip("\n")
            child_lines = child_inner.split("\n")
            lines.extend([f"> {line}" for line in child_lines])
        result = "\n".join(lines)
        return result + "\n"

# <body>
class Body(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("body", attrs)

    def to_str(self) -> str:
        return "\n".join(child.to_str() for child in self.children)


# <caption>
class Caption(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("caption", attrs)


# <code>
class Code(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("code", attrs)

    def detect_language(self) -> str:
        attr_cls = self.attr("class")
        # language-<lang> or lang-<lang>
        if m := re.search("(language|lang)-([a-z0-9]+)", attr_cls):
            return m.group(2)
        # language only
        for c in attr_cls.split(" "):
            if c in HIGHLIGHT_LANGUAGES:
                return c
        return ""

    def to_str(self) -> str:
        inner_lines = self.inner().split("\n")
        lang = self.detect_language()
        if len(inner_lines) == 1:
            return f"`{self.inner()}`"
        else:
            return f"```{lang}\n{self.inner()}```\n"


# <del>
class Del(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("del", attrs)

    def to_str(self) -> str:
        return f"~~{self.inner()}~~"


# <em>
class Em(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("em", attrs)

    def to_str(self) -> str:
        return f"*{self.inner()}*"


class H(Tag):
    def __init__(self, attrs: Attr, h_num: int) -> None:
        super().__init__(f"h{h_num}", attrs)
        self.h_num = h_num

    def to_str(self) -> str:
        return f"{'#' * self.h_num} {self.inner()}\n"


# <hr>
class Hr(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("hr", attrs)

    def to_str(self) -> str:
        return "---\n"


# <img>
class Img(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("img", attrs)

    def to_str(self) -> str:
        alt = self.attr("alt")
        src = self.attr("src")
        return f"![{alt}]({src})"


# <ul>
class Ul(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("ul", attrs)

    def append_child(self, child: Element) -> None:
        if isinstance(child, Content):
            raise ValueError("")

        if not child.name in ["li", "ul", "ol"]:
            raise ValueError("")
        if isinstance(child, Li):
            child.mark = "-"
        self.children.append(child)

    def to_str(self) -> str:
        lines = []
        for child in self.children:
            lines.extend([f"  {s}\n" for s in child.to_str().rstrip().split("\n")])
        return "".join(lines)


# <ol>
class Ol(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("ol", attrs)

    def append_child(self, child: Element) -> None:
        if isinstance(child, Content):
            raise ValueError("")

        if not child.name in ["li", "ul", "ol"]:
            raise ValueError("")
        if isinstance(child, Li):
            child.mark = f"1."
        self.children.append(child)

    def to_str(self) -> str:
        lines = []
        for child in self.children:
            lines.extend([f"  {s}\n" for s in child.to_str().rstrip().split("\n")])
        return "".join(lines)


# <li>
class Li(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("li", attrs)
        self.mark = ""

    def to_str(self) -> str:
        return f"{self.mark} {self.inner()}"


# <p>
class P(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("p", attrs)

    def to_str(self) -> str:
        return f"{self.inner()}\n"


# <span>
class Span(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("span", attrs)


# <strong>
class Strong(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("strong", attrs)

    def to_str(self) -> str:
        return f"**{self.inner()}**"


# <table>
class Table(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("table", attrs)
        self.head: Optional[Thead] = None
        self.body: Optional[Tbody] = None
        self.tmp_tr: List[Tr] = []
        self.caption: Optional[Caption] = None

    def append_child(self, child: Element) -> None:
        if isinstance(child, Content):
            raise ValueError()

        # invalid tag
        if child.name not in ["tr", "thead", "tbody", "caption", "colgroup"]:
            raise ValueError()

        if isinstance(child, Tr):
            if self.head is None:
                head = Thead(child.attrs)
                head.append_child(child)
                self.head = head
            else:
                self.tmp_tr.append(child)
        if isinstance(child, Thead):
            self.head = child
        elif isinstance(child, Caption):
            self.caption = child
        elif isinstance(child, Tbody):
            self.body = child

    def create_body_from_tr(self) -> None:
        self.body = Tbody({})
        for tr in self.tmp_tr:
            self.body.append_child(tr)

    def to_str(self) -> str:
        if not self.body and self.tmp_tr:
            self.create_body_from_tr()
        if not self.head and not self.body:
            return ""
        head = cast(Thead, self.head)
        body = cast(Tbody, self.body)
        caption = f"{self.caption.inner()}\n" if self.caption else ""
        # append body
        table = "\n".join(elem.to_str() for elem in [head, body])
        return caption + table + "\n"


# <tr>
class Tr(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("tr", attrs)

    def to_str(self) -> str:
        return "|" + "|".join(child.to_str() for child in self.children) + "|"


# <th>
class Th(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("th", attrs)


# <td>
class Td(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("td", attrs)


# <thead>
class Thead(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("thead", attrs)
        self.col_num = 0

    def append_child(self, child: Element) -> None:
        if isinstance(child, Content):
            raise ValueError()
        # only allow <tr>
        if not isinstance(child, Tr):
            raise ValueError()
        self.children.append(child)

    def to_str(self) -> str:
        # length of td or th
        col_num = 0
        if self.children and isinstance(self.children[-1], Tr):
            col_num = len(self.children[-1].children)
        if col_num:
            head_line = f"|{'|'.join(['---'] * col_num)}|"
            return self.inner() + "\n" + head_line
        else:
            return self.inner()


# <tbody>
class Tbody(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("tbody", attrs)

    def to_str(self) -> str:
        return "\n".join(child.to_str() for child in self.children)


# <pre>
class Pre(Tag):
    def __init__(self, attrs: Attr) -> None:
        super().__init__("pre", attrs)


# tag dict
TAG_CLS = {
    "a": A,
    "b": B,
    "br": Br,
    "blockquote": Blockquote,
    "body": Body,
    "caption": Caption,
    "code": Code,
    "del": Del,
    "em": Em,
    "hr": Hr,
    "html": HTML,
    "img": Img,
    "ul": Ul,
    "ol": Ol,
    "li": Li,
    "p": P,
    "span": Span,
    "strong": Strong,
    "table": Table,
    "thead": Thead,
    "tbody": Tbody,
    "tr": Tr,
    "th": Th,
    "td": Td,
    "pre": Pre,
}
