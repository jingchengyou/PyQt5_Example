"""
恢复面板
"""
import os

from PyQt5.QtWidgets import *

from view.recovery_dialog import Ui_Dialog
from control.logic.backup_new_task import init_folder

from control.tool.operate_thread import RecoveryThread


class RecoveryDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.files = list()

        self.path = init_folder()
        self.init_items()

        self.process_file = self.files[0] if self.files else None
        self.comboBox.activated.connect(self.item_slot)
        self.buttonBox.accepted.connect(self.recovery)

    def init_items(self):
        for root, dirs, file in os.walk(self.path):
            for per in file:
                self.comboBox.addItem(per)
                self.files.append(per)

    def item_slot(self, signal: int):
        if not self.files:
            return
        self.process_file = self.files[signal]

    def recovery(self):
        button_reply = QMessageBox.question(self, '提示', f'此操作将导致现有新程序{self.process_file}脚本丢失，'
                                                        f'且无法找回！停止操作请点击No',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if button_reply == QMessageBox.No:
            return
        else:
            print(self.process_file)
            thread = RecoveryThread(self.parent, self.process_file, self.path)
            thread.start()


if __name__ == "__main__":
    pass


