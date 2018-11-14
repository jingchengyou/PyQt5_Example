"""
主程序
操作各种逻辑和面板工具
"""
import sys

from PyQt5.QtWidgets import *

from view.main import Ui_MainWindow

from control.logic import *
logger = Logger(__name__).get_logger()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.keyword = ''

        self.old = None
        self.new = None

        self.searchLine.returnPressed.connect(self.search)
        self.searchButton.clicked.connect(self.search)
        self.importButton.clicked.connect(self.direct_import)
        self.newImportButton.clicked.connect(self.new_import)
        self.coverButton.clicked.connect(self.cover_import)
        self.recoveryButton.clicked.connect(self.recovery_new_task)
        self.deleteButton.clicked.connect(self.delete_new_task)

    def search(self):
        self.keyword = int(self.searchLine.text().strip())
        search = FindTask()
        self.old = search.get_old(task_id=self.keyword)
        self.new = search.get_old(task_id=self.keyword)
        if self.old:
            old_plain_text = f"老程序中存在taskid为{self.keyword}的脚本\n"
        else:
            old_plain_text = f"老程序中 不 存在taskid为{self.keyword}的脚本\n"
        if self.new:
            new_plain_text = f"新程序中存在taskid为{self.keyword}的脚本\n"
        else:
            new_plain_text = f"新程序中 不 存在taskid为{self.keyword}的脚本\n"
        plain_test = old_plain_text + new_plain_text
        self.textEdit.setText(plain_test)

    def direct_import(self):
        pass

    def new_import(self):
        pass

    def cover_import(self):
        pass

    def recovery_new_task(self):
        pass

    def delete_new_task(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


