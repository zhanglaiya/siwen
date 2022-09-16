import functools
import os

from flask import Flask, render_template
from . import confparser
from .core import get_files
from .markdown import Markdown

conf = confparser.read()
content_path = os.path.join(os.getcwd(), 'content')
content_path_length = len(content_path)

app = Flask(
    __name__,
    static_folder=os.path.join(os.getcwd(), 'themes', conf['project'].get('theme', 'default'), 'static'),
    template_folder=os.path.join(os.getcwd(), 'themes', conf['project'].get('theme', 'default'), 'templates')
)


@app.route('/')
def index():
    posts = []
    for file in get_files(content_path, ext='.md'):
        md = Markdown(file)
        settings = md.pop_settings()
        settings['href'] = file[content_path_length:].replace('\\', '/').replace('.md', '')
        posts.append(settings)

    return render_template('index.html', **conf, posts=posts)


def post(data):
    def view_func():
        return render_template('post.html', **data)
    return view_func


def add_post_rule():
    for file in get_files(content_path, ext='.md'):
        md = Markdown(file)
        rule = file[content_path_length:].replace('\\', '/').replace('.md', '')
        app.add_url_rule(
            rule,
            endpoint=rule,
            view_func=post(md.parse())
        )
