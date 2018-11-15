"""
将各个操作都直接封装到线程中
"""
import os
from threading import Thread
from time import sleep
from random import randint

from PyQt5.QtWidgets import *
from control.logic import TaskImport, FindTask, CoverTask, DeleteTask, Recovery, CornJob
from control.tool.process_bar import Bar


class BarThread(Thread):
    def __init__(self, parent):
        super().__init__()
        self.bar = Bar(parent)

    def speed(self):
        i = 1
        while i < 100:
            i += randint(1, 10)
            sleep(.5)
            self.bar.setValue(i)
        if i > 99:
            self.bar.setValue(100)
            sleep(1)
            self.bar.hide()

    def run(self):
        self.bar.show()
        self.speed()


class DirectThread(Thread):
    def __init__(self, parent=None, keyword=None, data=None):
        super().__init__()
        self.parent = parent
        self.keyword = keyword
        self.data = data

    def run(self):
        find_task = FindTask()
        new = find_task.get_new(int(self.keyword))
        if new:
            QMessageBox.information(self.parent, '提示', f'新程序中已存在taskid={self.keyword}的脚本，若想继续导入，请退出选择覆盖导入')
        else:
            insert_task = TaskImport()
            QMessageBox.information(self.parent, '提示', '脚本已成功从旧程序导入到新程序')
            if not insert_task.insert_task(self.data):
                QMessageBox.warning(self.parent, '警告', 'Sorry, 因网络或其他原因，直接导入操作失败，请稍后再试，或联系技术人员')


class NewThread(Thread):
    def __init__(self, parent=None, keyword=None, data=None):
        super().__init__()
        self.parent = parent
        self.keyword = keyword
        self.data = data

    def run(self):
        find_task = FindTask()
        new = find_task.get_new(int(self.keyword))
        if new:
            QMessageBox.information(self.parent, '提示', f'新程序中已存在taskid={self.keyword}的脚本，若想继续导入，请退出选择覆盖导入')
        else:
            insert_task = TaskImport()
            QMessageBox.information(self.parent, '提示', f'成功插入{self.keyword}脚本')
            if not insert_task.insert_different_task(task=int(self.keyword), data=self.data):
                QMessageBox.warning(self.parent, '警告', 'Sorry, 因网络或其他原因, 新建导入操作失败，请稍后再试，或联系技术人员')


class CoverThread(Thread):
    def __init__(self, parent=None, source=None, s_target=None):
        super().__init__()
        print(source)
        print(s_target)
        self.parent = parent
        self.source = int(source)
        self.target = int(s_target)

    def run(self):
        cover = CoverTask()
        find = FindTask()
        if not find.get_new(self.target):
            QMessageBox.information(self.parent, '提示', f'新程序没有{self.target}脚本，请采用直接导入或新建导入')
            return
        if self.source == self.target:
            QMessageBox.information(self.parent, '提示', '覆盖成功')
            if not cover.cover_task(self.source):
                QMessageBox.warning(self.parent, '警告', 'Sorry, 因网络或其他原因, 覆盖导入操作失败，请稍后再试，或联系技术人员')
        else:
            QMessageBox.information(self.parent, '提示', '覆盖成功')
            if not cover.cover_task(self.source, self.target):
                QMessageBox.warning(self.parent, '警告', 'Sorry, 因网络或其他原因, 覆盖导入操作失败，请稍后再试，或联系技术人员')


class DeleteThread(Thread):
    def __init__(self, parent=None, task=None):
        super().__init__()
        self.parent = parent
        self.task_id = int(task)

    def run(self):
        find = FindTask()
        if not find.get_new(self.task_id):
            QMessageBox.information(self.parent, '提示', f'新程序没有{self.task_id}脚本')
            return
        delete = DeleteTask()
        QMessageBox.information(self.parent, '提示', f'{self.task_id}删除成功')
        if not delete.delete_task(self.task_id):
            QMessageBox.warning(self.parent, '警告', 'Sorry, 因网络或其他原因, 删除新程序操作失败，请稍后再试，或联系技术人员')


class RecoveryThread(Thread):
    def __init__(self, parent=None, task=None, path=None):
        super().__init__()
        self.parent = parent
        self.task = int(task)
        self.path = path

    def run(self):
        work = Recovery()
        QMessageBox.information(self.parent, '提示', '恢复成功')
        if not work.recovery_task(self.task):
            QMessageBox.information(self.parent, '提示', '因源文件被修改或网络原因，操作失败，请稍后操作或联系技术人员')
        else:
            os.remove((self.path + '\\' + str(self.task)))


class CornThread(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        corn = CornJob()
        corn.execute_corn()

if __name__ == "__main__":
    pass


