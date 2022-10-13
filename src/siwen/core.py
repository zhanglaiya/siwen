import os
import configparser


def get_files(path, ext=None):
    for s in os.listdir(path):
        p = os.path.join(path, s)
        if os.path.isfile(p):
            if ext is None or p.endswith(ext):
                yield p
        else:
            for t in get_files(p, ext=ext):
                yield t


class Siwen:

    CWD = os.getcwd()
    ContentPath = os.path.join(CWD, 'content')
    Themes = 'themes'
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Siwen, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.serverName = None
        self.theme = None
        self.theme_path = None
        self.conf = None
        self.static = None
        self.template = None
        self.parse_config()

    def parse_config(self):
        config_file_path = os.path.join(self.CWD, 'config.ini')
        if not os.path.exists(config_file_path):
            raise OSError(f'当前路径下未检测到config.ini主配置文件')
        config = configparser.ConfigParser()
        config.read(config_file_path)
        if 'project' not in config:
            pass
        else:
            project = config['project']

            self.theme = project.get('theme', 'default')
            self.theme_path = os.path.join(self.CWD, self.Themes, self.theme)
            if os.path.isfile(self.theme_path):
                with open(self.theme_path, 'r', encoding='utf8') as f:
                    self.theme_path = os.path.join(self.CWD, self.Themes, f.read().strip())

            self.serverName = project.get('server-name', 'localhost')

            self.static = os.path.join(self.theme_path, 'static')
            self.template = os.path.join(self.theme_path, 'templates')
        self.conf = config

    def get_content_files(self):
        return get_files(
            self.ContentPath,
            ext='.md'
        )


g = Siwen()


if __name__ == '__main__':
    pass
