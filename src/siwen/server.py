import functools
import os

from flask import Flask, render_template
from . import confparser
from .core import get_files
from .markdown import Markdown

conf = confparser.read()

app = Flask(
    __name__,
    static_folder=os.path.join(os.getcwd(), 'themes', conf['project'].get('theme', 'default'), 'static'),
    template_folder=os.path.join(os.getcwd(), 'themes', conf['project'].get('theme', 'default'), 'templates')
)


@app.route('/')
def index():
    return render_template('index.html', **conf)


def content(data):
    def view_func():
        return render_template('post.html', **data)
    return view_func


content_path = os.path.join(os.getcwd(), 'content')
content_path_length = len(content_path)
for file in get_files(content_path, ext='.md'):
    md = Markdown(file)
    rule = file[content_path_length:].replace('\\', '/').replace('.md', '')
    app.add_url_rule(
        rule,
        endpoint=rule,
        view_func=content(md.parse())
    )
