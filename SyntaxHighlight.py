from PyQt5.QtCore import QRegExp

from PyQt5.QtGui import (
    QSyntaxHighlighter, 
    QTextCharFormat, 
    QFont, 
    QColor
)

class PyHighlight(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PyHighlight, self).__init__(parent)
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