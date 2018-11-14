"""
备份新程序中某个任务ID 的脚本
config/backup中存放
若没有，则在本地新建文件夹
"""
import os

from db.mysql import Mysql
from db.config import NEW_CONFIG


def init_folder():
    path = 'D:\\JetBrains\\person\\old_to_new\\config\\backup'
    if os.path.exists(path):
        return path
    else:
        temp_path = os.getcwd() + '\\old_to_new\\config\\backup'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        return temp_path


def mkdir(path_name: str) -> str:
    if not os.path.exists(path_name):
        os.mkdir(path_name)


class Backup:
    """
    备份数据；
    如有data，则表示显示备份保存该数据；
    若没有，则必须直接从数据库中取出数据并进行保存
    """
    def __init__(self, task: int, data: tuple =None):
        self.mysql = Mysql(NEW_CONFIG)
        self.task_name = str(task)
        self.backup_data = data
        self.path = init_folder() + '\\'

        self.file = self.path + self.task_name

    def backup_new_task(self):
        if not self.backup_data:
            back_sql = f"SELECT * FROM script WHERE taskid = {self.task_name} ORDER BY sort;"
            result = self.mysql.select(sql=back_sql)
            if not result:
                return False
            self.backup_data = str(result)
        mkdir(self.path)
        with open(self.file, mode='w', encoding='utf-8') as f:
            f.write(self.backup_data)
            return True


if __name__ == "__main__":
    # from control.logic.find_task_id import FindTask
    # find_task_temp = FindTask()
    # result_temp = find_task_temp.get_new(4109)

    back = Backup(6025)
    print(back.backup_new_task())



