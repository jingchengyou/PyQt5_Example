"""
dialog
将操作中相应步骤需要的数据用dialog的形式提示用户
"""
from PyQt5.QtWidgets import *


from view.message import Ui_Dialog


class Message(QDialog, Ui_Dialog):
    def __init__(self, parent=None, title: str=None, prompt: str=None):
        super().__init__(parent)
        self.setupUi(self)

        self.enable = False

        if title:
            self.setWindowTitle(title)
        if prompt:
            self.lineEdit.setPlaceholderText(prompt)

        self.buttonBox.accepted.connect(self.format_confirm)

    def format_confirm(self):
        keyword = self.lineEdit.text().strip()
        if keyword == '':
            QMessageBox.warning(self, '警告', '待插入的taskid不能为空')
        elif not keyword.isdigit():
            QMessageBox.warning(self, '警告', '新程序的taskid由数字组成')
        else:
            self.enable = True


if __name__ == "__main__":
    message = Message()
    message.show()
    message.exec_()


