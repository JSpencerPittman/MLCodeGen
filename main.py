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
    QMainWindow,
    QTextEdit
)
from PyQt5.QtCore import Qt, QSize, QRegExp
from PyQt5.QtGui import QIcon, QSyntaxHighlighter, QTextCharFormat, QFont, QTextOption, QColor

import sys, os
from filetree import FileTree
import pyperclip

# class MyHighlighter(QSyntaxHighlighter):
#     def highlightBlock(self, text):
#         myClassFormat = QTextCharFormat()
#         myClassFormat.setFontWeight(QFont.Bold)
#         myClassFormat.setForeground(Qt.darkMagenta)
#         pattern = "\\bMy[A-Za-z]+\\b"

#         expression = QRegExp(pattern)
#         index = text.indexOf(expression)
#         while index >= 0:
#             length = expression.matchedLength()
#             self.setFormat(index, length, myClassFormat)
#             index = text.indexOf(expression, index + length)

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)
        self.highlighting_rules = []
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor('#00AA00'))
        keywords = ['if', 'else', 'while', 'for', 'in', 'break', 'continue', 'return', 'def', 'class', 'import', 'from']
        for word in keywords:
            pattern = "\\b" + word + "\\b"
            rule = QTextCharFormat()
            rule.setForeground(QColor('#00AA00'))
            rule.setFontWeight(QFont.Bold)
            self.highlighting_rules.append((QRegExp(pattern), rule))
    
    def highlightBlock(self, text):
        for pattern, rule in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule)
                index = expression.indexIn(text, index + length)

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
code_display_content = QTextEdit("")
code_display_content.setWordWrapMode(QTextOption.WrapMode.NoWrap)
highlighter = Highlighter(code_display_content.document())
#code_display_content.textChanged.connect(highlighter.rehighlight)

right_v_lay.addWidget(code_display_content)
code_display.setLayout(right_v_lay)
#scroll.setWidget(code_display)
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
#copy_button.clicked.connect(highlighter.rehighlight)
copy_button.setIcon(QIcon('copy.png'))
copy_button.setIconSize(QSize(40,40))

main_h_lay = QHBoxLayout()
main_h_lay.setContentsMargins(30,30,30,30)
main_h_lay.setSpacing(20)
main_h_lay.addWidget(tree)
main_h_lay.addWidget(code_display)
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