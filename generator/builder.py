from os import listdir
from os.path import isfile, join
from jinja2 import Environment, FileSystemLoader, select_autoescape
from post import Post, PostRef
from typing import Generator
from tomllib import load
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from email.utils import format_datetime

class Builder:
    src: str
    dst: str
    postDir: str
    title: str
    url: str
    date: datetime
    page_env: Environment
    snippet_env: Environment
    rss_env: Environment

    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst
        with open("config.toml", "rb") as f:
            config = load(f)
        
        self.title = config['title']
        self.url = config['url']
        self.date = datetime.now(tz=ZoneInfo("Europe/Amsterdam"))
        self.date = self.date.astimezone(timezone.utc)

        self.postDir = join(self.src, "posts")
        self.page_env = Environment(
            loader=FileSystemLoader(join(src, "templates", "pages")),
            autoescape=select_autoescape()
        )
        self.snippet_env = Environment(
            loader=FileSystemLoader(join(src, "templates", "snippets")),
            autoescape=select_autoescape()
        )
        self.rss_env = Environment(
            loader=FileSystemLoader(join(src, "templates", "rss")),
            autoescape=select_autoescape()
        )
    
    def build(self):
        posts = self.generatePosts()
        self.generateHome(posts)
        self.generateRssFeed(posts)

    def getPosts(self) -> Generator[Post, None, None]:
        for f in listdir(self.postDir):
            if isfile(join(self.postDir, f)):
                yield Post(join(self.postDir, f))

    def generatePosts(self) -> list[PostRef]:
        template = self.page_env.get_template("post.html")

        posts: list[PostRef] = []
        
        for post in self.getPosts():
            with open(join(self.dst, "posts", f"{post.filename}.html"), 'w') as f:
                f.write(post.generate(template))
            posts.append(post.reference())
        
        return posts

    def generateHome(self, posts: list[PostRef]):
        pageTemplate = self.page_env.get_template("index.html")
        itemTemplate = self.snippet_env.get_template("post-list-item.html")

        postsHtml = [itemTemplate.render(filename=post.filename, title=post.title) for post in posts]
        pageHtml = pageTemplate.render(index="\n".join(postsHtml))
        with open(join(self.dst, "index.html"), 'w') as f:
            f.write(pageHtml)
    
    def generateRssFeed(self, posts):
        rssTemplate = self.rss_env.get_template("feed.xml")
        with open(join(self.dst, "feed.xml"), 'w') as f:
            rssFeed = rssTemplate.render(title=self.title, url=self.url, buildDate=format_datetime(self.date), posts=posts)
            f.write(rssFeed)
                
