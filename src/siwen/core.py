import os


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


if __name__ == '__main__':

    for i in get_files(r'C:\Users\User\example_siwen\content'):
        print(i)
