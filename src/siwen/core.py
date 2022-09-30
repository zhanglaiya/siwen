import os
from .confparser import read

class Siwen:
    pass


def get_files(path, ext=None):
    for s in os.listdir(path):
        p = os.path.join(path, s)
        if os.path.isfile(p):
            if ext is None or p.endswith(ext):
                yield p
        else:
            for t in get_files(p, ext=ext):
                yield t


def get_theme_path(cur_path=None):
    if cur_path is None:
        cur_path = os.getcwd()
    conf = read()
    theme = conf['project'].get('theme', 'default')
    theme_path = os.path.join(cur_path, 'themes', theme)
    if os.path.isfile(theme_path):
        with open(theme_path, 'r') as f:
            theme_path = os.path.join(cur_path, 'themes', f.read().strip())
    return theme_path


if __name__ == '__main__':
    pass
