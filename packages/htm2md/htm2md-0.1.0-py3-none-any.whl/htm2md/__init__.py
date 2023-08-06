from .parser import Parser

__version__ = "0.1.0"


def convert(html: str) -> str:
    parser = Parser()
    parser.feed(html)

    result = []
    for elem in parser.parse_result:
        result.append(elem.to_str())
    return "\n".join(result)
