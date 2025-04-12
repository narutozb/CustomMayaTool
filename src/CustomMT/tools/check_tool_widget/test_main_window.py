import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("PySide6 演示窗口")
        self.setMinimumSize(600, 400)

        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
