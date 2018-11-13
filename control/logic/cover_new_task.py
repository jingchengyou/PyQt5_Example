"""
将老程序覆盖掉现有新程序

1、同名覆盖
2、异名覆盖

警告，必须备份,参考backup_new_task
"""

from control.logic.find_task_id import FindTask
from control.logic.delete_new_task import DeleteTask
from control.logic.new_task_import import TaskImport


class CoverTask:
    def __init__(self):
        super().__init__()

    @staticmethod
    def cover_task(source_task: int, target_task: int = None) -> bool:
        find_task = FindTask()
        source = find_task.get_old(task_id=source_task)
        delete_task = DeleteTask()
        if target_task:
            delete_result = delete_task.delete_task(task_id=target_task)  # 异名导入
            if source and delete_result:
                temp = list()
                for per in source:
                    per_list = list(per)
                    per_list[2] = target_task
                    temp.append(tuple(per_list))
                trans_source = tuple(temp)
                task_import = TaskImport()
                return task_import.insert_task(trans_source)
            else:
                False
        else:
            delete_result = delete_task.delete_task(task_id=source_task)  # 同名导入
            if source and delete_result:
                task_import = TaskImport()
                return task_import.insert_task(source)
            else:
                return False


if __name__ == "__main__":
    cover_task = CoverTask()
    print(cover_task.cover_task(4109, 6025))


