from jinja2 import Template


class HomePage:
    template: Template

    def __init__(self, template: Template):
        self.template = template
