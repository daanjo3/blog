from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.front_matter import front_matter_plugin

md = MarkdownIt(
    "commonmark",
    { 
        'html': True
}).use(front_matter_plugin).enable('table')

def parseFrontMatter(tokens: list[Token]) -> dict:
    metadata = dict()
    for token in tokens:
        if token.type != 'front_matter':
            continue
        entries = token.content.split("\n")
        metadata = dict()
        for entry in entries:
            data = entry.split(":")
            metadata[data[0].strip()] = data[1].strip()
    return metadata