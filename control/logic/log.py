"""
日志系统
config/log中存放，若没有，则本地新建文件夹存放
包含两部分：
1、本地异常测试
2、文本日志，以时间天数为单位

14天清除一次
"""
import os
import logging
from datetime import datetime

path_folder = 'D:\JetBrains\person\old_to_new\config\log'


def generate_folder():
    if os.path.exists(path_folder):
        return path_folder
    else:
        temp_path = os.getcwd() + '\old_to_new\config\log'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        return temp_path


filename = generate_folder() + '\\' + datetime.now().strftime("%Y%m%d")


class Logger:
    def __init__(self, keyword):
        super().__init__()
        if keyword:
            self.keyword = keyword
        else:
            self.keyword = __name__

    def get_logger(self):
        logger = logging.getLogger('O2N')
        logger.setLevel(level=logging.DEBUG)

        formatter = logging.Formatter(f"%(asctime)s - %(levelname)s - <{self.keyword}>:%(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S")

        # 将日志写入到文件中
        file_handler = logging.FileHandler(filename=filename)
        file_handler.setLevel(level=logging.WARNING)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 将日志写入到控制台中
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level=logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger


if __name__ == "__main__":
    # path_folder = generate_folder()
    # print(path_folder)
    test_logger = Logger(__name__).get_logger()
    test_logger.critical('fadafada')




