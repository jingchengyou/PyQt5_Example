"""
恢复新程序中的某个任务ID的脚本数据：
1、删除后的脚本恢复
2、覆盖后的脚本恢复

检验脚本数据格式是否是对的
包含覆盖功能 cover_new_task

策略：
1、根据taskid来决定恢复哪一个脚本
2、检查备份文件夹中是否有这个脚本
3、检验脚本格式是否有篡改
4、删除新数据库中对应脚本
5、导入
"""
import os
from control.logic.delete_new_task import DeleteTask
from control.logic.new_task_import import TaskImport
from control.logic.backup_new_task import init_folder

from control.logic.log import Logger
logger = Logger(__name__).get_logger()


class Recovery:
    def __init__(self):
        super().__init__()
        self.path = init_folder()

    @staticmethod
    def _confirm_format(task: int, data: str):
        try:
            input_data = tuple(eval(data))
            for per in input_data:
                if per[5] != task:
                    return False
        except Exception as e:
            logger.critical(e)
            return False
        else:
            return True

    def recovery_task(self, task: int):
        file = self.path + '\\' + str(task)
        if os.path.exists(file):
            with open(file, mode='r', encoding='utf-8') as f:
                file_data = f.read()
                print(file_data)
                if self._confirm_format(task, file_data):
                    print(file_data)
                    delete = DeleteTask()
                    if delete.delete_task(task_id=task, delete_switch=1):
                        import_task = TaskImport()
                        if import_task.insert_back(tuple(eval(file_data))):
                            return True
                        else:
                            return False
                else:
                    return False
        else:
            return False


if __name__ == "__main__":
    recovery = Recovery()
    print(recovery.recovery_task(6025))


