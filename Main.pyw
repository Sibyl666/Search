import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFormLayout, QListWidget, QPushButton, QSystemTrayIcon, \
    QLabel
from PyQt5.QtGui import QIcon, QKeyEvent
from PyQt5.QtCore import Qt
import configparser
import os
import re


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.lst = []
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Search")
        self.list = QListWidget()
        self.resetconfig = QPushButton("Reset Config To Default")
        self.flabel = QLabel('Found: 0')

        layout = QFormLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.list)
        layout.addWidget(self.resetconfig)
        layout.addWidget(self.flabel)
        self.setLayout(layout)

        self.edit.returnPressed.connect(self.search)
        self.resetconfig.clicked.connect(self.parseconfig)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.list.clear()
            self.edit.clear()

    def search(self):
        path = self.readconfig()
        searchname = self.edit.text()

        files = os.scandir(path['path'])
        for i in files:
            if re.search(searchname, i.path, re.IGNORECASE):
                self.lst.append(i.path)
        self.list.addItems(self.lst)
        self.flabel.setText("Found: " + str(self.list.count()))

    def parseconfig(self):
        config = configparser.ConfigParser()
        config['settings'] = {
            'path': 'D:\osu!\Songs',
            'width': '500',
            'height': '500'
        }
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    def readconfig(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        path = config['settings']
        return path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()

    wh = form.readconfig()
    form.setGeometry(200, 200, int(wh['width']), int(wh['height']))
    form.setWindowTitle('Search')
    form.setWindowIcon(QIcon('icons/Search.png'))
    QSystemTrayIcon(QIcon('icons/Search.png'))

    form.show()
    app.exec_()
