import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QLineEdit,
                               QTextEdit, QGroupBox, QComboBox)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont


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

        # 添加标题标签
        self.title_label = QLabel("PySide6 组件示例")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # 创建输入部分
        self.create_input_section()

        # 创建显示部分
        self.create_display_section()

        # 创建按钮部分
        self.create_button_section()

        # 连接信号和槽
        self.connect_signals()

    def create_input_section(self):
        """创建输入部分"""
        input_group = QGroupBox("输入")
        input_layout = QHBoxLayout()

        # 添加标签和文本输入框
        input_layout.addWidget(QLabel("姓名:"))
        self.name_input = QLineEdit()
        input_layout.addWidget(self.name_input)

        # 添加下拉选择框
        input_layout.addWidget(QLabel("选择:"))
        self.combo_box = QComboBox()
        self.combo_box.addItems(["选项1", "选项2", "选项3"])
        input_layout.addWidget(self.combo_box)

        input_group.setLayout(input_layout)
        self.main_layout.addWidget(input_group)

    def create_display_section(self):
        """创建显示部分"""
        display_group = QGroupBox("显示")
        display_layout = QVBoxLayout()

        # 添加文本编辑框
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        display_layout.addWidget(self.text_display)

        display_group.setLayout(display_layout)
        self.main_layout.addWidget(display_group)

    def create_button_section(self):
        """创建按钮部分"""
        button_layout = QHBoxLayout()

        # 添加按钮
        self.clear_button = QPushButton("清除")
        self.submit_button = QPushButton("提交")
        self.exit_button = QPushButton("退出")

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.exit_button)

        self.main_layout.addLayout(button_layout)

    def connect_signals(self):
        """连接信号和槽"""
        self.clear_button.clicked.connect(self.clear_inputs)
        self.submit_button.clicked.connect(self.submit_data)
        self.exit_button.clicked.connect(self.close)
        self.combo_box.currentIndexChanged.connect(self.selection_changed)

    @Slot()
    def clear_inputs(self):
        """清除输入"""
        self.name_input.clear()
        self.text_display.clear()

    @Slot()
    def submit_data(self):
        """提交数据"""
        name = self.name_input.text()
        selection = self.combo_box.currentText()

        if not name:
            self.text_display.setText("请输入姓名!")
            return

        display_text = f"姓名: {name}\n选择: {selection}"
        self.text_display.setText(display_text)

    @Slot(int)
    def selection_changed(self, index):
        """选择变更"""
        self.text_display.append(f"选择已更改为: {self.combo_box.currentText()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())