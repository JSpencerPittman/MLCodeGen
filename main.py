from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QHBoxLayout,
    QTreeWidgetItem,
    QLabel,
    QScrollArea,
    QVBoxLayout
)
from PyQt5.QtCore import Qt

import sys, os
from filetree import FileTree

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

#code_display.addScrollBarWidget(code_display_content, Qt.AlignmentFlag.AlignCenter)

main_h_lay = QHBoxLayout()
main_h_lay.addWidget(tree)
main_h_lay.addWidget(scroll)

window = QWidget()
window.setLayout(main_h_lay)
window.show()


app.exec()