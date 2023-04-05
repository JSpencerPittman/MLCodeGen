from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QMainWindow,
    QTextEdit,
    QBoxLayout,
    QListWidget,
    QListWidgetItem
)

from PyQt5.QtCore import QSize

from PyQt5.QtGui import QIcon, QTextOption

import sys, os
from SyntaxHighlight import PyHighlight
import pyperclip
from functools import partial

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
RECYCLED_CODE_DIR = "codestore"
CATEGORIES = ("Preprocessing","Visualization","Training",
              "Scoring","Utility")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout()

        self.code_display = QWidget()
        self.code_display_layout = QVBoxLayout()
        self.code_display_content = QTextEdit()

        self.selection_panel = QWidget()
        self.selection_panel_layout = QVBoxLayout()

        self.copy_button = QPushButton()


        self.init_copy_button()
        self.init_code_display()
        self.init_selection_panel()

        self.init_central_widget()
        self.init_main_layout()

        self.init_syntax_highlighter()

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("ML Code Recycler")

    def init_main_layout(self):
        self.main_layout.addWidget(self.selection_panel)
        self.main_layout.addWidget(self.code_display)
        self.main_layout.addWidget(self.copy_button)

        self.main_layout.setContentsMargins(30,30,30,30)
        self.main_layout.setSpacing(20)

    def init_central_widget(self):
        self.central_widget.setLayout(self.main_layout)

        self.central_widget.setProperty('class', 'PRIMARY_DARK')

    def init_selection_panel(self):
        self.selection_panel.setLayout(self.selection_panel_layout)
        
        self.selection_panel_layout.setContentsMargins(0,0,0,0)
        self.selection_panel_layout.setSpacing(30)

        for cat in CATEGORIES:
            cat_button = self.create_category_button(cat)
            self.selection_panel_layout.addWidget(cat_button)

    def load_selection_category(self, cat):
        self.clear_layout(self.selection_panel_layout)

        files = self.load_dir_files(cat)
    
        back_button = QPushButton(cat)
        back_button.clicked.connect(self.handle_selection_back_click)

        file_selection = QListWidget()
        for file in files:
            new_item = self.create_file_selection_item(cat, file)
            file_selection.addItem(new_item)
        file_selection.itemClicked.connect(partial(self.handle_file_selection_item_click, cat))
        
        back_button.setProperty('class', 'GREEN SELECTION_BUTTON')
        back_button.setMinimumSize(300, 100)

        file_selection.setProperty('class', 'SECONDARY_DARK FILE_SELECTION')
        file_selection.setSizePolicy(QSizePolicy.Policy.Minimum, 
                                    QSizePolicy.Policy.Expanding)

        self.selection_panel_layout.addWidget(back_button)
        self.selection_panel_layout.addWidget(file_selection)

    def create_file_selection_item(self, cat, file):
        item = QListWidgetItem()
        item.setText(self.make_file_name_pretty(file))
        return item

    def create_category_button(self, cat):
        cat_button = QPushButton(cat)

        cat_button.setSizePolicy(QSizePolicy.Policy.Minimum, 
                                QSizePolicy.Policy.Expanding)
        cat_button.setMinimumWidth(300)
        cat_button.setProperty('class', 'GREEN SELECTION_BUTTON')
        cat_button.clicked.connect(partial(self.handle_selection_button_click, cat))

        return cat_button

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
        self.copy_button.setProperty('class', 'GREEN COPY_BUTTON')
        self.copy_button.setIcon(QIcon('rsc/copy.png'))
        self.copy_button.setIconSize(QSize(40,40))

        self.copy_button.clicked.connect(self.copy_text_from_code_panel)

    def init_syntax_highlighter(self):
        self.syntax_highlighter = PyHighlight(self.code_display_content.document())

    def copy_text_from_code_panel(self):
         pyperclip.copy(self.code_display_content.toPlainText())
         pyperclip.paste()

    def handle_selection_button_click(self, cat):
        self.load_selection_category(cat)

    def handle_selection_back_click(self):
        self.clear_layout(self.selection_panel_layout)
        self.init_selection_panel()

    def handle_file_selection_item_click(self, cat, item: QListWidgetItem):
        file_name = self.make_file_name_ugly(item.text())
        file_path = RECYCLED_CODE_DIR + '/' + cat + '/' + file_name
        with open(file_path, 'r') as f:
            text = f.read()
        self.code_display_content.setText(text)

    def make_file_name_pretty(self, file_name:str):
        file_name = file_name[:file_name.index('.')]
        file_name = [word.capitalize() for word in file_name.split('_')]
        file_name = " ".join(file_name)
        return file_name
    
    def make_file_name_ugly(self, file_name:str):
        file_name = file_name.lower()
        file_name = file_name.split(' ')
        file_name = "_".join(file_name)
        file_name += '.py'
        return file_name

    def load_dir_files(self, directory):
        path = RECYCLED_CODE_DIR + '/' + directory
        
        if not os.path.isdir(path):
            return []
        
        return os.listdir(path)
    
    def clear_layout(self, layout: QBoxLayout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    # Add Stylesheet
    with open("style.css", 'r') as f:
        app.setStyleSheet(f.read())

    window.show()

    app.exec()