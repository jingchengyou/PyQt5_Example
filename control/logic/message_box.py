"""
弹框提示信息
主要包含各种操作后对应的信息弹框展示
"""
from PyQt5.QtWidgets import *


from control.logic.log import Logger
logger = Logger(__name__).get_logger()


class MessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.addButton('good')
        self.critical("ceshi")


if __name__ == "__main__":
    box = MessageBox()
    box.show()

