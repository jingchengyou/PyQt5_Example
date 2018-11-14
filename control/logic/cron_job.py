"""
定时任务。
定时删除备份的脚本、日志
"""
import os
from datetime import datetime
from control.logic.backup_new_task import init_folder
from control.logic.log import generate_folder


class CornJob:
    def __init__(self, log_corn: int=7, back_corn: int=7):
        super().__init__()
        self.back_path = init_folder()
        self.log_path = generate_folder()
        self.log_deadline = log_corn
        self.back_deadline = back_corn

        self.execute_corn()

    def corn_log(self):
        jobs = list()
        for root, dirs, file in os.walk(self.log_path):
            for per in file:
                atime = os.path.getatime(root + '\\' + per)
                atime_struct = datetime.fromtimestamp(atime)
                delay = datetime.now().day - atime_struct.day
                if delay > self.log_deadline:
                    jobs.append(root + '\\' + per)
        return jobs

    def corn_back(self):
        jobs = list()
        for root, dirs, file in os.walk(self.back_path):
            for per in file:
                atime = os.path.getatime(root + '\\' + per)
                atime_struct = datetime.fromtimestamp(atime)
                delay = datetime.now().day - atime_struct.day
                if delay > self.back_deadline:
                    jobs.append(root + '\\' + per)
        return jobs

    def execute_corn(self):
        log = self.corn_log()
        if log:
            for per in log:
                os.remove(per)
        back = self.corn_back()
        if back:
            for per in back:
                os.remove(per)


if __name__ == "__main__":
    corn = CornJob()
    # print(corn.corn_log())
    # print(corn.corn_back())
    # print(corn.execute_corn())


