import os
import json

from flask import Flask
from .core import get_theme_path, get_files
from .markdown import Markdown
from . import confparser


class Build:
    path = os.getcwd()


conf = confparser.read()
theme_dir_path = os.path.join(os.getcwd(), 'themes')
theme_name = conf['project'].get('theme', 'default')

theme = os.path.join(theme_dir_path, theme_name)
if not os.path.exists(theme):
    raise OSError(f'{theme} 主题路径不存在')


if os.path.isfile(theme):
    with open(theme, 'r') as f:
        theme = os.path.join(theme_dir_path, f.read().strip())

app = Flask(
    __name__,
    static_folder=os.path.join(theme, 'static'),
    template_folder=os.path.join(theme, 'templates')
)
app.config['SERVER_NAME'] = '127.0.0.1'


def generate_html():
    cur_path = os.getcwd()
    # theme = get_theme_path(cur_path=cur_path)
    # templates = os.path.join(theme, 'templates')
    # env = Environment(loader=FileSystemLoader(templates))  # 加载模板
    # index = env.get_template('index.html')
    # post = env.get_template('post.html')
    # # template.stream(body).dump('result.html', 'utf-8')
    index = app.jinja_env.get_or_select_template('index.html')
    post = app.jinja_env.get_or_select_template('post.html')
    docs = os.path.join(cur_path, 'docs')
    result = os.path.join(docs, 'index.html')

    posts = []
    for file in get_files(os.path.join(cur_path, 'content'), ext='.md'):
        md = Markdown(file)
        data = md.parse()
        relative_path = file[len(cur_path):].replace('\\', '/')
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
