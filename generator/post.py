from pathlib import Path

from jinja2 import Template
from markdown import md, parseFrontMatter
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from email.utils import format_datetime

class PostRef:
    title: str
    date: str
    dateRss: str
    path: Path
    filename: str

    def __init__(self, title: str, date: str, path: Path):
        self.title = title
        self.date = date
        
        dt = datetime.strptime(date, "%d-%m-%Y")
        dt = dt.replace(tzinfo=timezone.utc)
        self.dateRss = format_datetime(dt)

        self.path = path
        self.filename = path.stem

class Post:
    title: str
    date: str

    markdown: str
    html: str

    path: Path
    filename: str

    def __init__(self, path: str):
        print(path)
        with open(path, 'r') as f:
            self.markdown = f.read()

        self.path = Path(path)
        self.filename = self.path.stem
        
        self.html = md.render(self.markdown)
        
        tokens = md.parse(self.markdown)
        metadata = parseFrontMatter(tokens)
        
        if "title" not in metadata:
            raise Exception(f"post at {path} is missing a title")
        if "date" not in metadata:
            raise Exception(f"post at {path} is missing a date")
        self.title = metadata["title"]
        self.date = metadata["date"]
    
    def generate(self, template: Template) -> str:
        return template.render(
            title=self.title,
            date=self.date,
            content=self.html
        )
    
    def reference(self) -> PostRef:
        return PostRef(self.title, self.date, self.path)
