import sys
from PyQt5.QtWidgets import *


class Bar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)

        self.setValue(1)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        style = """
                        QProgressBar {
                            border: 3px solid grey;
                            border-radius: 5px;
                            text-align: center;
                        }
                        QProgressBar::chunk {
                            background-color: #00ff00;
                            width: 20px;
                        }"""
        self.setStyleSheet(style)

        self.setGeometry(500, 500, 200, 25)
        self.resize(200, 25)
        self.center()

    def center(self):
        screen = self.parent.geometry()
        self.move((screen.width()-200)/2, (screen.height()-25)/5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bar = Bar()
    bar.show()
    sys.exit(app.exec_())
