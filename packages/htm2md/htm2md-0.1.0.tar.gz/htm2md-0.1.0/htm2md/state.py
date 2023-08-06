from dataclasses import dataclass, field
from typing import List, Optional

from .tag import Element, Tag


@dataclass
class ParserState:
    tag_stack: List[Tag] = field(default_factory=list)
    unhandeld_tags: List[str] = field(default_factory=list)
    in_pre: bool = False

    def current_tag_name(self) -> str:
        if self.tag_stack:
            return self.tag_stack[-1].name
        return ""

    def current_tag(self) -> Optional[Tag]:
        if self.tag_stack:
            return self.tag_stack[-1]
        return None
