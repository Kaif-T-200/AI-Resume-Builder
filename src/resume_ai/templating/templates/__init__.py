from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_template_env():
    templates_dir = Path(__file__).parent
    loader = FileSystemLoader(str(templates_dir))
    env = Environment(loader=loader, autoescape=select_autoescape(["html", "xml"]))
    return env
