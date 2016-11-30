import os.path
from piratetools42.redmineapi import Issue
from jinja2 import Template, Environment
from jinja2.loaders import FileSystemLoader

here = os.path.dirname(__file__)
print(here)

jinja_env = Environment(loader=FileSystemLoader(os.path.join(here, "templates")))

def protocol_from_issue(issue):
    return jinja_env.get_template("default_protocol.j2.md").render(**issue)
