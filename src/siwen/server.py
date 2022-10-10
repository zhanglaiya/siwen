import os

from flask import Flask, render_template
from .markdown import Markdown
from siwen.core import get_files


class Server:

    def __init__(self, path, static_folder, template_folder):
        self.path = path
        self.content_path = os.path.join(path, 'content')
        self.app = Flask(
            __name__,
            static_folder=static_folder,
            template_folder=template_folder
        )

    def config_set(self, k, v):
        self.app.config[k] = v

    def get_or_select_template(self, *args, **kwargs):
        return self.app.jinja_env.get_or_select_template(*args, **kwargs)

    def add_url_rule(self, conf):
        posts = []

        def post(data):
            def view_func():
                return render_template('post.html', **data)

            return view_func

        for file in get_files(self.content_path):
            md = Markdown(file)
            settings = md.pop_settings()
            rule = file[len(self.content_path):].replace('\\', '/').replace('.md', '')
            settings['href'] = rule
            posts.append(settings)
            self.app.add_url_rule(
                rule,
                endpoint=rule,
                view_func=post(md.parse())
            )

        def index():
            return render_template('index.html', **conf, posts=posts)

        self.app.add_url_rule(
            '/',
            endpoint='/',
            view_func=index
        )

    def run(self):
        self.app.run(
            host='localhost',
            port=1228,
            debug=True,
            extra_files=get_files(self.path)
        )
