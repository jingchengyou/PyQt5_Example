"""
查找新、旧数据库中对应的任务id脚本
"""
from db.mysql import Mysql
from db.config import OLD_CONFIG, NEW_CONFIG


old_sql = ("SELECT tag_name, sort, taskid, xpath, value, action, precode "
           "FROM gms_tags WHERE taskid= %s ORDER BY sort;")
new_sql = ("SELECT tag_name, sort, taskid, xpath, value, action, precode "
           "FROM script WHERE taskid= %s ORDER BY sort;")
old_db = Mysql(OLD_CONFIG)
new_db = Mysql(NEW_CONFIG)


class FindTask:
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_old(task_id: int) -> tuple:
        return old_db.select(old_sql, (task_id,))

    @staticmethod
    def get_new(task_id: int) -> tuple:
        return new_db.select(new_sql, (task_id,))


if __name__ == "__main__":
    find_task = FindTask()
    oo = find_task.get_old(4109)
    nn = find_task.get_new(4109)
    print(oo)
    print(type(oo))
    print(nn)
    print(type(nn))


