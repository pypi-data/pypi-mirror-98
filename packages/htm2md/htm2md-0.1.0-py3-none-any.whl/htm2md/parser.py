import re
from html import unescape
from html.parser import HTMLParser
from typing import List, Optional, Tuple, cast

from .const import SELF_CLOSING_TAGS
from .state import ParserState
from .tag import *


class Parser(HTMLParser):
    def feed(self, feed: str) -> None:
        self.state = ParserState()
        self.parse_result: List[Element] = []
        super().feed(feed)

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        dict_attrs = dict(attrs)

        if tag == "pre":
            self.state.in_pre = True

        # construct new tag
        if tag in TAG_CLS:
            tag_class = TAG_CLS[tag]
            new_tag = tag_class(dict_attrs)
        elif m := re.match("h([1-6])", tag):
            h_num = int(m.group(1))
            new_tag = H(dict_attrs, h_num)
        else:
            # unhandled tag
            if tag not in SELF_CLOSING_TAGS:
                self.state.unhandeld_tags.append(tag)
            return

        # append new tag to current tag
        curr_tag = self.state.current_tag()
        if curr_tag:
            curr_tag.append_child(new_tag)

        if tag not in SELF_CLOSING_TAGS:
            self.state.tag_stack.append(new_tag)
            return

        if not self.state.tag_stack:
            self.parse_result.append(new_tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in SELF_CLOSING_TAGS:
            return

        if self.state.unhandeld_tags and tag == self.state.unhandeld_tags[-1]:
            self.state.unhandeld_tags.pop()
            return

        if tag == "pre":
            self.state.in_pre = False

        if len(self.state.tag_stack) != 1:
            self.state.tag_stack.pop()
            return

        if tag == self.state.current_tag_name():
            self.parse_result.append(self.state.tag_stack.pop())

    def handle_data(self, data: str) -> None:
        if self.state.unhandeld_tags:
            return

        # unescape data
        data = unescape(data)

        # trim space and LF
        if not self.state.in_pre:
            data = re.sub(r"\n\s+$", "", data)
            data = data.strip("\n")
            if not data:
                return

        if not self.state.tag_stack:
            self.parse_result.append(Content(data))
            return
        curr_tag = self.state.tag_stack[-1]
        curr_tag.append_child(Content(data))
