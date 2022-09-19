import os
import configparser


def read():
    cur_path = os.getcwd()
    config_file_path = os.path.join(cur_path, 'config.ini')
    if not os.path.exists(config_file_path):
        raise OSError(f'当前路径下未检测到config.ini主配置文件')
    config = configparser.ConfigParser()
    config.read(config_file_path)
    if 'project' not in config:
        pass
    else:
        print(config['project'])
    return config
