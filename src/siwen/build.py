import os
import json

from jinja2 import Environment, FileSystemLoader
from .core import get_theme_path, get_files
from .markdown import Markdown
from . import confparser


class Build:
    path = os.getcwd()

def generate_html():
    cur_path = os.getcwd()
    theme = get_theme_path(cur_path=cur_path)
    templates = os.path.join(theme, 'templates')
    env = Environment(loader=FileSystemLoader(templates))  # 加载模板
    template = env.get_template('index.html')
    # # template.stream(body).dump('result.html', 'utf-8')

    docs = os.path.join(cur_path, 'docs')
    result = os.path.join(docs, 'index.html')
    print(result)
    posts = []
    for file in get_files(cur_path, ext='.md'):
        md = Markdown(file)
        settings = md.pop_settings()
        settings['href'] = file[len(cur_path):].replace('\\', '/').replace('.md', '')
        posts.append(settings)
    conf = confparser.read()

    with open(result, 'w') as fout:

        html_content = template.render(**conf, posts=posts)
        fout.write(html_content)  # 写入模板 生成html
