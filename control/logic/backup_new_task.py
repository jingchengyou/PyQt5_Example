"""
备份新程序中某个任务ID 的脚本
config/backup中存放
若没有，则在本地新建文件夹
"""
import os
from datetime import datetime

folder = datetime.now().strftime('%Y%m%d')


def init_folder():
    path = 'D:\\JetBrains\\person\\old_to_new\\config\\backup'
    if os.path.exists(path):
        return path
    else:
        temp_path = os.getcwd() + '\\old_to_new\\config\\backup'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        return temp_path


class Backup:
    def __init__(self, task: int, data: tuple):
        self.task_name = str(task)
        self.backup_data = data

        self.file = init_folder() + '\\' + folder + '\\' + self.task_name

    def backup_new_task(self):
        pass


if __name__ == "__main__":
    pass


