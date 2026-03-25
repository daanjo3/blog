from os import listdir
from os.path import isfile, join
from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.front_matter import front_matter_plugin
from jinja2 import Environment, FileSystemLoader, select_autoescape

md = MarkdownIt("commonmark", { 'html': True}).use(front_matter_plugin).enable('table')

class Builder:
    src: str
    dst: str
    postDir: str
    env: Environment
    md: MarkdownIt

    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst
        self.postDir = join(self.src, "posts")
        self.env = Environment(
            loader=FileSystemLoader(join(src, "templates")),
            autoescape=select_autoescape()
        )

    def getPosts(self) -> list[str]:
        return [f for f in listdir(self.postDir) if isfile(join(self.postDir, f))]

    def getPostContent(self, postName) -> str:
        content = None
        with open(join(self.postDir, postName), 'r') as f:
            content = f.read()
        if content == None:
                raise "Failed to read markdown"
        return content

    def getPostMetadata(self, postName, tokens=None) -> dict:
        if (tokens == None):
            content = self.getPostContent(postName)
            tokens = md.parse(content)
        return parseFrontMatter(tokens)

    def generatePosts(self):    
        template = self.env.get_template("post.html")
        
        for fileName in self.getPosts():
            contentMd = self.getPostContent(fileName)
            metadata = self.getPostMetadata(fileName, tokens=md.parse(contentMd))

            contentHtml = md.render(contentMd)
            
            fileNameClean = fileName.split(".")[0]
            fileNameCleanFull = f"{fileNameClean}.html"
            title = metadata["title"] if fileNameClean in metadata else fileNameClean
            
            pageHtml = template.render(title=title, content=contentHtml)

            with open(join(self.dst, "posts", fileNameCleanFull), 'w') as f:
                f.write(pageHtml)

    def generateHome(self):
        template = self.env.get_template("index.html")

        postsHtml = ['<ul class="post-list">']
        for fileName in self.getPosts():
            metadata = self.getPostMetadata(fileName)
            fileNameClean = fileName.split(".")[0]
            title = metadata["title"] if fileNameClean in metadata else fileNameClean
            postsHtml.append(f'<li><a href="posts/{fileNameClean}.html">{title}</a></li>')
        postsHtml.append('</ul>')

        pageHtml = template.render(index="\n".join(postsHtml))
        with open(join(self.dst, "index.html"), 'w') as f:
            f.write(pageHtml)

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
