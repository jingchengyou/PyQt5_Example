"""
主程序
操作各种逻辑和面板工具
"""
import sys

from PyQt5.QtWidgets import *

from view.main import Ui_MainWindow

from control.tool import *
from control.logic import *
logger = Logger(__name__).get_logger()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.keyword = ''

        corn_thread = CornThread()
        corn_thread.setDaemon(True)
        corn_thread.start()

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

        self.keyword = int(self.searchLine.text().strip()) if self.searchLine.text() else ''
        if not self.keyword:
            QMessageBox.warning(self, '提示', '请输入旧程序taskid，以查找新、旧程序是否存在该脚本')
            return
        search = FindTask()
        self.old = search.get_old(task_id=self.keyword)
        self.new = search.get_new(task_id=self.keyword)
        if self.old:
            old_plain_text = f"<p>老程序中<span style='font-size:12pt; color:#ff5500;'>存   在</span>" \
                             f"taskid=<span style='font-size:12pt; color:#ff5500;'>{self.keyword}</span>的脚本</p>"
        else:
            old_plain_text = f"<p>老程序中<span style='font-size:12pt; color:#ff5500;'>不存在</span>" \
                             f"taskid=<span style='font-size:12pt; color:#ff5500;'>{self.keyword}</span>的脚本</p>"
        if self.new:
            new_plain_text = f"<p>新程序中<span style='font-size:12pt; color:#ff5500;'>存   在</span>" \
                             f"taskid=<span style='font-size:12pt; color:#ff5500;'>{self.keyword}</span>的脚本</p>"
        else:
            new_plain_text = f"<p>新程序中<span style='font-size:12pt; color:#ff5500;'>不存在</span>" \
                             f"taskid=<span style='font-size:12pt; color:#ff5500;'>{self.keyword}</span>的脚本</p>"
        plain_test = old_plain_text + new_plain_text
        self.textEdit.setText(plain_test)

    def direct_import(self):
        if not self.old:
            QMessageBox.information(self, '提示', '请先查询旧程序是否存在将被导入的脚本')
            return
        if not self.new:
            thread = DirectThread(self, keyword=self.keyword, data=self.old)
            thread.start()
        else:
            QMessageBox.information(self, '提示', f'新程序已存在{self.keyword}脚本')

    def new_import(self):
        if not self.old:
            QMessageBox.information(self, '提示', '请先查询旧程序是否存在将被导入的脚本')
            return
        message = Message(self, title='新建导入', prompt='请输入新程序中待插入的taskid')
        message.exec_()

        if message.enable:
            keyword = message.lineEdit.text().strip()
            thread = NewThread(parent=self, keyword=keyword, data=self.old)
            thread.start()

    def cover_import(self):
        if not self.old:
            QMessageBox.information(self, '提示', '请先查询旧程序是否存在将被导入的脚本')
            return
        QMessageBox.critical(self, '严重警告', '此操作可能导致新程序脚本丢失，请谨慎操作')
        QMessageBox.warning(self, '提示', f"此操作将在'{init_folder()}'下备份被覆盖脚本，7日内可恢复")
        message = Message(self, title='覆盖导入', prompt='请输入新程序中待覆盖的taskid')
        message.exec_()
        if message.enable:
            keyword = message.lineEdit.text().strip()
            thread = CoverThread(self, source=self.keyword, s_target=keyword)
            thread.start()

    def recovery_new_task(self):
        QMessageBox.warning(self, '警告', '此操作可能导致新程序脚本丢失，请谨慎操作')
        recovery = RecoveryDialog(self)
        recovery.exec_()

    def delete_new_task(self):
        QMessageBox.critical(self, '严重警告', '此操作可能导致新程序脚本丢失，请谨慎操作')
        QMessageBox.warning(self, '提示', f"此操作将在'{init_folder()}'下备份被删除脚本，7日内可恢复")
        message = Message(self, '删除新程序', '请输入新程序中待删除的taskid')
        message.exec_()
        if message.enable:
            keyword = message.lineEdit.text().strip()
            thread = DeleteThread(self, keyword)
            thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


