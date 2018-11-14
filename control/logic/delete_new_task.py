"""
删除新程序中某个任务ID的脚本！
旧程序中脚本若删除，必须联系技术人员

严重警告
必须备份，参考backup_new_task
"""
from db.mysql import Mysql
from db.config import NEW_CONFIG

from control.logic.backup_new_task import Backup


class DeleteTask:
    """
    根据taskid，来删除新程序某个脚本，且在删除之前会检验新程序是否有脚本，若有，则先备份再删除
    """
    def __init__(self):
        super().__init__()
        self.mysql = Mysql(NEW_CONFIG)

    def delete_task(self, task_id: int, delete_switch: int=0) -> bool:
        """
        根据taskid删除新程序脚本
        :param task_id: 对应脚本taskid
        :param delete_switch: 默认为0，则删除新程序时自动备份；若为1，则不备份
        :return: bool，若为false，则表示新程序没有该脚本，删除失败；若为真，则表示删除成功
        """
        if not delete_switch:
            back = Backup(task=task_id)
            if not back.backup_new_task():
                return False
        sql = f"DELETE FROM script WHERE taskid = {task_id}"
        return self.mysql.delete(sql=sql)


if __name__ == "__main__":
    delete_task = DeleteTask()
    print(delete_task.delete_task(6025))


