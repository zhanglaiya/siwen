import os

from .core import g, get_files
from .server import Server
from .markdown import Markdown


class Builder:

    def __init__(self):
        self.server = Server()

    def set_server_name(self, server_name):
        self.server.config_set('SERVER_NAME', server_name)

    def generate_html(self, conf):
        index = self.server.get_or_select_template('index.html')
        post = self.server.get_or_select_template('post.html')
        docs = os.path.join(g.CWD, 'docs')
        result = os.path.join(docs, 'index.html')

        posts = []
        for file in get_files(g.ContentPath):
            md = Markdown(file)
            data = md.parse()
            relative_path = file[len(g.ContentPath):].replace('\\', '/')
            post_relative_dir = relative_path.strip('/').replace('.md', '')

            tmp_base = docs
            for i in post_relative_dir.split('/'):
                if not os.path.exists(os.path.join(tmp_base, i)):
                    os.mkdir(os.path.join(tmp_base, i))
                tmp_base = os.path.join(tmp_base, i)

            post_save = os.path.join(docs, post_relative_dir, 'index.html')
            # print(docs, post_relative_path, post_save)
            data['settings']['href'] = relative_path.replace('.md', '')
            posts.append(data['settings'])
            with open(post_save, 'w', encoding='utf8') as fout:
                html_content = post.render(**data)
                fout.write(html_content)  # 写入模板 生成html

        with open(result, 'w', encoding='utf8') as fout:

            html_content = index.render(**conf, posts=posts)
            fout.write(html_content)  # 写入模板 生成html
