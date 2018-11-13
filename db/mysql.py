"""
@author: Scott
@time: 2018-11-09
@purpose: connect mysql by this module.

python >= 2.7 or python >=3.4
MySQL >= 5.5
"""
import requests
from control.logic.log import Logger
import pymysql
from pymysql.err import Error, OperationalError
from contextlib import contextmanager

logger = Logger(__name__).get_logger()


def confirm_network(func):
    def wrapper(*args, **kwargs):
        try:
            r = requests.get("http://www.baidu.com", timeout=30)
            logger.debug("正在测试网络")
            if r.status_code == 200:
                logger.debug("网络情况优秀")
        except Exception as e:
            logger.warning(f"<_confirm_network.exception>-网络失去连接,详情错误：{e}")
            return -1  # 网络失去连接
        else:
            return func(*args, **kwargs)
    return wrapper


class Mysql:
    def __init__(self, kwargs: dict):
        super().__init__()
        self.error = None
        self.config = kwargs

    @contextmanager
    def _connect(self):
        db = pymysql.connect(**self.config)
        try:
            yield db
        except OperationalError as e:
            logger.critical(f"<_connect.OperationError>-{e}")
        except Error as e:
            logger.critical(f"<_connect.Error>-{e}")
        finally:
            if db:
                db.commit()
                db.close()

    def _execute(self, sql: str):
        with self._connect() as db:
            try:
                cursor = db.cursor()
                cursor.execute(sql)
            except OperationalError as e:
                db.rollback()
                logger.critical(f"<_execute.OperationError>-{e}")
            except Error as e:
                db.rollback()
                logger.critical(f"<_execute.Error>-{e}")
            else:
                return cursor

    def _execute_many(self, sql: str, data: tuple):
        with self._connect() as db:
            try:
                cursor = db.cursor()
                cursor.executemany(sql, data)
            except OperationalError as e:
                db.rollback()
                logger.critical(f"<_execute_many.OperationError>-{e}")
            except Error as e:
                db.rollback()
                logger.critical(f"<_execute_many.Error>-{e}")
            else:
                return cursor

    @confirm_network
    def select(self, sql: str, data: tuple =tuple()) -> tuple:
        if data:
            return self._execute_many(sql=sql, data=data).fetchall()
        else:
            return self._execute(sql=sql).fetchall()

    @confirm_network
    def insert(self, sql: str, data: tuple =tuple()) -> bool:
        if data:
            if self._execute_many(sql=sql, data=data):
                return True
        else:
            if self._execute(sql=sql):
                return True

    @confirm_network
    def update(self, sql: str, data: tuple =tuple()) -> bool:
        if data:
            if self._execute_many(sql=sql, data=data):
                return True
        else:
            if self._execute(sql=sql):
                return True

    @confirm_network
    def delete(self, sql: str, data: tuple =tuple()) -> bool:
        if data:
            if self._execute_many(sql=sql, data=data):
                return True
        else:
            if self._execute(sql=sql):
                return True


if __name__ == "__main__":
    from db.config import MYSQL_CONFIG
    mysql = Mysql(MYSQL_CONFIG)
    # SQL = "SELECT username FROM test.users"
    # print(mysql._connect())
    # print(mysql._execute(SQL))
    # print(mysql.select(SQL))
    sql2 = 'SELECT username FROM test.users WHERE password = %s'
    data1 = ('12345600',)
    print(mysql._execute_many(sql=sql2, data=data1))
    # print(mysql._execute('SELECT username FROM test.users WHERE password = "%s"' % '12345600'))
    print(mysql.select(sql=sql2, data=data1))
    #
    # sql3 = "INSERT INTO test.users (username, password) VALUES (%s, %s)"
    # data3 = (("wu王的女人", "good"),)
    # print(mysql.insert(sql=sql3, data=data3))
    #
    # sql4 = "UPDATE test.users SET username = 'good傻子', password = '3badboy' WHERE id = %s"
    # data4 = ((31,),)
    # print(mysql.update(sql=sql4, data=data4))
    #
    # sql5 = "DELETE FROM test.users WHERE password = %s"
    # data5 = (('good',),)
    # print(mysql.delete(sql5, data5))





