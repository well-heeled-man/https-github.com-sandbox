#!/usr/bin/python

'''
Basic PyQT GUI.
'''
#pylint: disable=no-name-in-module

import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QGridLayout, QVBoxLayout, QWidget)

class Window(QWidget):
    ''' Main window class '''

    def __init__(self):

        super(Window, self).__init__()

        input_label = QLabel("Enter the size in bytes:")

        self.input_line = QLineEdit()
        self.input_line.returnPressed.connect(self.result)
        self.input_line.returnPressed.connect(self.input_line.clear)

        self.submit_button = QPushButton("Calculate")
        self.submit_button.clicked.connect(self.result)
        self.submit_button.clicked.connect(self.input_line.clear)

        button_layout = QVBoxLayout()
        button_layout.addWidget(input_label)
        button_layout.addWidget(self.input_line)
        button_layout.addWidget(self.submit_button)

        main_layout = QGridLayout()
        main_layout.addLayout(button_layout, 0, 1)

        self.setLayout(main_layout)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Byte Converter")

    def result(self):
        ''' Result popup '''

        value = self.input_line.text()

        if not value.isdigit():
            QMessageBox.information(self, "Error", "Please enter a size in bytes")
            return
        else:
            size = self.human_readable(float(value))
            QMessageBox.information(self, "Result", size)

    @staticmethod
    def human_readable(value):
        ''' human_readable result '''

        terabyte = value / 1000**4
        gigabyte = value / 1000**3
        megabyte = value / 1000**2
        kilobyte = value / 1000

        if terabyte > 1:
            human_value = "{} TiB".format(round(terabyte, 2))
        elif gigabyte > 1:
            human_value = "{} GiB".format(round(gigabyte, 2))
        elif megabyte > 1:
            human_value = "{} MiB".format(round(megabyte, 2))
        elif kilobyte > 1:
            human_value = "{} KiB".format(round(kilobyte, 2))
        else:
            human_value = "{} B".format(value)

        return human_value

def main():
    ''' Main '''

    app = QApplication(sys.argv)

    screen = Window()
    screen.show()

    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
