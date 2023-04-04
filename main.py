from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QHBoxLayout,
    QTreeWidgetItem,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QPushButton,
    QSizePolicy
)
from PyQt5.QtCore import Qt

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

code_display = QWidget()
scroll = QScrollArea()
right_v_lay = QVBoxLayout()
code_display_content = QLabel("Right Side")

right_v_lay.addWidget(code_display_content)
code_display.setLayout(right_v_lay)
scroll.setWidget(code_display)

scroll.setWidgetResizable(True)
scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

copy_button = QPushButton("Copy")
copy_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
copy_button.setMinimumSize(50,100)
copy_button.setStyleSheet('QPushButton { transform: rotate(270deg); }')
copy_button.clicked.connect(copy_text)

main_h_lay = QHBoxLayout()
main_h_lay.setContentsMargins(30,30,30,30)
main_h_lay.setSpacing(20)
main_h_lay.addWidget(tree)
main_h_lay.addWidget(scroll)
main_h_lay.addWidget(copy_button)


window = QWidget()
window.setLayout(main_h_lay)
window.setFixedSize(1400,800)
window.show()


app.exec()