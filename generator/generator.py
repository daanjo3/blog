from os import listdir
from os.path import isfile, join
from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.front_matter import front_matter_plugin
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
md = MarkdownIt("commonmark", { 'html': True}).use(front_matter_plugin).enable('table')
postDir = "posts"

def parseFrontMatter(tokens: list[Token]) -> dict:
    for token in tokens:
        if token.type != 'front_matter':
            continue
        entries = token.content.split("\n")
        metadata = dict()
        for entry in entries:
            data = entry.split(":")
            metadata[data[0].strip()] = data[1].strip()
        return metadata

def getPosts() -> list[str]:
    return [f for f in listdir(postDir) if isfile(join(postDir, f))]

def getPostContent(postName) -> str:
    content = None
    with open(join(postDir, postName), 'r') as f:
        content = f.read()
    if content == None:
            raise "Failed to read markdown"
    return content

def getPostMetadata(postName, tokens=None) -> dict:
    if (tokens == None):
        content = getPostContent(postName)
        tokens = md.parse(content)
    return parseFrontMatter(tokens)

def generatePosts():    
    template = env.get_template("post.html")
    
    for fileName in getPosts():
        contentMd = getPostContent(fileName)
        metadata = getPostMetadata(fileName, tokens=md.parse(contentMd))

        contentHtml = md.render(contentMd)
        
        fileNameClean = fileName.split(".")[0]
        title = metadata["title"] if fileNameClean in metadata else fileNameClean
        
        pageHtml = template.render(title=title, content=contentHtml)

        with open(f"./build/posts/{fileNameClean}.html", 'w') as f:
            f.write(pageHtml)

def generateHome():
    template = env.get_template("index.html")

    postsHtml = ['<ul>']
    for fileName in getPosts():
        metadata = getPostMetadata(fileName)
        fileNameClean = fileName.split(".")[0]
        title = metadata["title"] if fileNameClean in metadata else fileNameClean
        postsHtml.append(f'<li><a href="posts/{fileNameClean}.html">{title}</a></li>')
    postsHtml.append('</ul>')

    pageHtml = template.render(index="\n".join(postsHtml))
    with open(f"./build/index.html", 'w') as f:
        f.write(pageHtml)


generatePosts()
generateHome()