import os, sys
from PyQt5.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem
)

class FileTree(object):
    def __init__(self, path):
        self.path = path
        self.tree = {}

    def create_file_tree(self, trim=False):
        for root, dirs, files in os.walk(self.path, topdown=True):
           root = root.split('\\')[-1]
           self.tree[root] = dirs.copy()
           self.tree[root].append(files)

        while trim:
            del_keys = []
            for k,v in self.tree.items():
                if len(v) == 1 and len(v[0]) == 0:
                    del_keys.append(k)

            trim = True if len(del_keys) > 0 else False
            for k in del_keys:
                del self.tree[k]

    def get_qt_tree(self, click_cb):
        qt_tree = QTreeWidget()

        for top_level_item in self.tree[self.path][:-1]:
            if top_level_item in self.tree.keys():
                qt_tree.addTopLevelItem(self.get_tree_item(top_level_item))

        qt_tree.itemClicked.connect(click_cb)
        return qt_tree

    def get_tree_item(self, loc):
        item = QTreeWidgetItem([loc])
        
        # Add subdirectories
        for child in self.tree[loc][:-1]:
            if child in self.tree.keys():
                item.addChild(self.get_tree_item(child))

        # Add files
        for file in self.tree[loc][-1]:
            item.addChild(QTreeWidgetItem([file]))

        return item