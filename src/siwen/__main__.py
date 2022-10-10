import os
import argparse
import configparser

from siwen import __version__

from siwen.core import Siwen
from siwen.build import Builder
from siwen.server import Server


INIT_CONTENT = '''---
title:hello siwen
draft:true
---'''


def get_version():
    return __version__


def _theme(args):

    print(os.getcwd())
    print(args.theme_name, 'theme')


def _site(args):

    root_path = os.path.abspath(args.site_name)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    else:
        raise OSError(f'{root_path}不是空目录')

    config_file_path = os.path.join(root_path, 'config.ini')
    config = configparser.ConfigParser()
    config['project'] = {
        'title': 'hello world',
        'base_url': 'http://zhanglaiya.github.io/siwen'
    }
    with open(config_file_path, 'w', encoding='utf8') as f:
        config.write(f)


def create_post(path):
    abspath = os.path.abspath(path)
    dirname = os.path.dirname(abspath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(abspath, 'w') as f:
        f.write(INIT_CONTENT)


def _server():
    xsw = Siwen()
    xsw.parse_config()
    server = Server(xsw.CWD, xsw.static, xsw.template)
    server.add_url_rule(xsw.conf)
    server.run()


def _build():
    xsw = Siwen()
    xsw.parse_config()
    builder = Builder(xsw.CWD, xsw.static, xsw.template)
    builder.set_server_name(xsw.serverName)
    builder.generate_html(xsw.conf)


def parse_args():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title='子命令', metavar='')

    new = subparsers.add_parser(name='new', help='新建 站点/主题')
    dev = subparsers.add_parser(name='server', help='启动开发服务器')
    dev.set_defaults(dev=_server)
    bld = subparsers.add_parser(name='build', help='编译生成html')
    bld.set_defaults(bld=_build)
    new.add_argument('post_path')
    new_subparsers = new.add_subparsers(title='可用的子命令')
    site = new_subparsers.add_parser('site', help='新建站点')
    theme = new_subparsers.add_parser('theme', help='新建主题')

    site.add_argument('site_name')
    site.set_defaults(new=_site)
    theme.add_argument('theme_name')
    theme.set_defaults(new=_theme)

    parser.add_argument('-v', '--version', dest='version', action='store_true', help='获取版本')
    return parser.parse_args()


def main():
    args = parse_args()
    # print(args)
    if hasattr(args, 'new'):
        args.new(args)
    elif hasattr(args, 'dev'):
        args.dev()
    elif hasattr(args, 'bld'):
        args.bld()
    elif hasattr(args, 'post_path'):
        create_post(args.post_path)
    elif args.version:
        print(get_version())
    else:
        _build()


if __name__ == '__main__':
    main()
