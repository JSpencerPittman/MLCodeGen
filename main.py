from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QHBoxLayout,
    QTreeWidgetItem,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QMainWindow
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

import sys, os
from filetree import FileTree
import pyperclip

code_display = None
code_display_content = None

def get_text_file(path):
    with open(path, 'r') as f:
        return f.read()

def handle_item_click(item : QTreeWidgetItem, col:int):
    # If a directory ignore it
    if item.childCount() > 0:
        return
    
    path = item.text(0)
    parent = item.parent()
    while parent:
        path = parent.text(0) + '/' + path
        parent = parent.parent()
    path = "codestore/" + path

    print(path)
    text = get_text_file(path)
    code_display_content.setText(text)

def copy_text():
    pyperclip.copy(code_display_content.text())
    pyperclip.paste()

app = QApplication(sys.argv)

# Create File Tree Structure
ft = FileTree("codestore")
ft.create_file_tree(trim=True)
tree = ft.get_qt_tree(handle_item_click)
tree.setHeaderLabel("CodeStore")
tree.setProperty('class', 'SECONDARY_DARK TREE_VIEW')
tree.setHeaderHidden(True)

code_display = QWidget()
scroll = QScrollArea()
right_v_lay = QVBoxLayout()
code_display_content = QLabel("")

right_v_lay.addWidget(code_display_content)
code_display.setLayout(right_v_lay)
scroll.setWidget(code_display)
scroll.setProperty('class', 'SCROLL')
code_display_content.setProperty('class', 'CODE_CONTENT')
code_display.setProperty('class', 'SECONDARY_DARK')

scroll.setWidgetResizable(True)
scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

v_scrollbar = scroll.verticalScrollBar()

h_scrollbar = scroll.horizontalScrollBar()

copy_button = QPushButton()
copy_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
copy_button.setMinimumSize(70,100)
copy_button.setProperty('class', 'GREEN')
copy_button.clicked.connect(copy_text)
copy_button.setIcon(QIcon('copy.png'))
copy_button.setIconSize(QSize(40,40))

main_h_lay = QHBoxLayout()
main_h_lay.setContentsMargins(30,30,30,30)
main_h_lay.setSpacing(20)
main_h_lay.addWidget(tree)
main_h_lay.addWidget(scroll)
main_h_lay.addWidget(copy_button)


window = QMainWindow()
central_widget = QWidget()
central_widget.setLayout(main_h_lay)
central_widget.setFixedSize(1400,800)
central_widget.setProperty('class', 'PRIMARY_DARK')
window.setCentralWidget(central_widget)
window.setWindowTitle("ML Code Recycle")
window.show()

with open("style.qss", 'r') as f:
    app.setStyleSheet(f.read())

app.exec()