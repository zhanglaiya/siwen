from flask import Flask, render_template
from .markdown import Markdown
from .core import g, get_files


class Server:

    def __init__(self):
        self.content_path = g.ContentPath
        self.app = Flask(
            __name__,
            static_folder=g.static,
            template_folder=g.template
        )

    def config_set(self, k, v):
        self.app.config[k] = v

    def get_or_select_template(self, *args, **kwargs):
        return self.app.jinja_env.get_or_select_template(*args, **kwargs)

    def add_url_rule(self):
        posts = []

        def post(data):
            def view_func():
                return render_template('post.html', **data)

            return view_func

        for file in get_files(g.ContentPath):
            md = Markdown(file)
            settings = md.pop_settings()
            rule = file[len(g.ContentPath):].replace('\\', '/').replace('.md', '')
            settings['href'] = rule
            posts.append(settings)
            self.app.add_url_rule(
                rule,
                endpoint=rule,
                view_func=post(md.parse())
            )

        def index():
            return render_template('index.html', **g.conf, posts=posts)

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
            extra_files=get_files(g.CWD)
        )
