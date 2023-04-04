from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QHBoxLayout,
    QTreeWidgetItem,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QMainWindow,
    QTextEdit,
    QTreeWidget
)

from PyQt5.QtCore import QSize

from PyQt5.QtGui import QIcon, QTextOption

import sys
from filetree import FileTree
from SyntaxHighlight import PyHighlight
import pyperclip

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
RECYCLED_CODE_DIR = "codestore"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout()

        self.tree_view = QTreeWidget()
        
        self.code_display = QWidget()
        self.code_display_layout = QVBoxLayout()
        self.code_display_content = QTextEdit()

        self.copy_button = QPushButton()

        self.init_tree_view()
        self.init_copy_button()
        self.init_code_display()

        self.init_central_widget()
        self.init_main_layout()

        self.init_syntax_highlighter()

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("ML Code Recycler")

    def init_main_layout(self):
        self.main_layout.addWidget(self.tree_view)
        self.main_layout.addWidget(self.code_display)
        self.main_layout.addWidget(self.copy_button)

        self.main_layout.setContentsMargins(30,30,30,30)
        self.main_layout.setSpacing(20)

    def init_central_widget(self):
        self.central_widget.setLayout(self.main_layout)

        self.central_widget.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.central_widget.setProperty('class', 'PRIMARY_DARK')

    def init_tree_view(self):
        file_tree = FileTree(RECYCLED_CODE_DIR)
        file_tree.create_file_tree(trim=True)
        self.tree_view = file_tree.get_qt_tree(self.handle_tree_item_click)
        self.tree_view.setProperty('class', 'SECONDARY_DARK TREE_VIEW')
        self.tree_view.setHeaderHidden(True)

    def init_code_display(self):
        self.code_display.setLayout(self.code_display_layout)
        self.code_display.setProperty('class', 'SECONDARY_DARK')
        
        self.code_display_layout.addWidget(self.code_display_content)

        self.code_display_content.setProperty('class', 'CODE_CONTENT')
        self.code_display_content.setWordWrapMode(QTextOption.WrapMode.NoWrap)

    def init_copy_button(self):
        self.copy_button.setSizePolicy(QSizePolicy.Policy.Minimum, 
                                       QSizePolicy.Policy.Expanding)
        self.copy_button.setMinimumSize(70,100)
        self.copy_button.setProperty('class', 'GREEN')
        self.copy_button.setIcon(QIcon('copy.png'))
        self.copy_button.setIconSize(QSize(40,40))

        self.copy_button.clicked.connect(self.copy_text_from_code_panel)

    def init_syntax_highlighter(self):
        self.syntax_highlighter = PyHighlight(self.code_display_content.document())

    def copy_text_from_code_panel(self):
         pyperclip.copy(self.code_display_content.text())
         pyperclip.paste()

    def handle_tree_item_click(self, item : QTreeWidgetItem, col:int):
        # If a directory ignore it
        if item.childCount() > 0:
            return
        
        path = item.text(0)
        parent = item.parent()
        while parent:
            path = parent.text(0) + '/' + path
            parent = parent.parent()
        path = RECYCLED_CODE_DIR + '/' + path

        with open(path, 'r') as f:
            text = f.read()
        self.code_display_content.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    # Add Stylesheet
    with open("style.qss", 'r') as f:
        app.setStyleSheet(f.read())

    window.show()

    app.exec()