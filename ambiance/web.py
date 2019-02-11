from sanic import Blueprint
from sanic.response import html
from jinja2 import Environment, PackageLoader, select_autoescape

bp = Blueprint(__name__)
env = Environment(loader=PackageLoader('web', 'templates'), autoescape=select_autoescape(['html', 'xml']))


@bp.route('/')
def root():
    template = env.get_template('index.j2')
    content = template.render()
    return html(content)

