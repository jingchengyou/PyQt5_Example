"""
往新程序插入旧程序数据
"""
from db.mysql import Mysql
from db.config import NEW_CONFIG


class TaskImport:
    """
    将tuple类型的数据导入到新程序中，不需要taskid
    """
    def __init__(self):
        super().__init__()
        self.mysql = Mysql(NEW_CONFIG)

    def insert_task(self, data: tuple):
        sql = (f"INSERT INTO script (tag_name, sort, taskid, xpath, value, action, precode)"
               f"VALUES (%s, %s, %s, %s, %s, %s, %s)")
        return self.mysql.insert(sql=sql, data=data)


if __name__ == "__main__":
    from control.logic.find_task_id import FindTask

    find_task = FindTask()
    result = find_task.get_old(6025)
    print(result)
    print(type(result))

    task_import = TaskImport()
    print(task_import.insert_task(result))


