
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import re


class TextHighLight(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, plainText, firstDate, secondDate):
        datePattern = "^[0-9]{4}\\-[0-9]{1,2}\\-[0-9]{1,2}"
        systemPattern = "system"
        email = "populpock2@gmail.com"

        cursor = QTextCursor(plainText.document())
        for line in plainText.toPlainText().splitlines():
            match = re.search(datePattern, line)
            
            if match != None:
                if self.checkDate(match.group(), firstDate, secondDate):
                    match = re.search(systemPattern, line, re.IGNORECASE)
                    if match != None:
                        plainText.insertPlainText(" " + email + " \t")

                        cursor.movePosition(QTextCursor.StartOfLine)
                        plainText.setTextCursor(cursor)
                        cursor.setPosition(cursor.position() + len(email) + 2, QTextCursor.KeepAnchor)
                        
                        fmt = QTextCharFormat()
                        fmt.setBackground(Qt.cyan)
                        cursor.setCharFormat(fmt)

            cursor.movePosition(QTextCursor.Down)
            plainText.setTextCursor(cursor)                        
            cursor.movePosition(QTextCursor.StartOfLine)
            plainText.setTextCursor(cursor)


    def checkDate(self, currentDateText, firstDate, secondDate):
        try:
            currentDate = datetime.datetime.strptime(currentDateText, '%Y-%m-%d')
            if firstDate <= currentDate.date() <= secondDate:
                return True
            else:
                return False
        except ValueError as err:
            print("Wrong date input: " + str(err))


def loadfile(plainText):
    filePath, _ = QFileDialog.getOpenFileName(window, "Load file", "", "")
    if filePath == "":
        return
    text = open(filePath).read()
    plainText.setPlainText(text)

if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Parser [Lab04 PyQt]")
    window.resize(700, 500)
    window.show()

    plainText = QPlainTextEdit()
    SearchHighLights = TextHighLight(plainText.document())
    
    btn_open = QPushButton('Открыть файл')
    btn_open.clicked.connect(lambda: loadfile(plainText))

    inputDateFirst = QDateEdit()
    inputDateFirst.setCalendarPopup(True)
    inputDateFirst.setDate(QDate(2022, 1, 1))

    inputDateSecond = QDateEdit()
    inputDateSecond.setCalendarPopup(True)
    inputDateSecond.setDate(QDate(2023, 11, 1))

    btn_search = QPushButton(' Поиск словоформ по дате')
    btn_search.clicked.connect(lambda: SearchHighLights.parse(plainText, inputDateFirst.date().toPyDate(), inputDateSecond.date().toPyDate()))


    grid = QGridLayout()
    grid.addWidget(btn_open, 0, 0)
    grid.addWidget(inputDateFirst, 0, 1)
    grid.addWidget(inputDateSecond, 0, 2)
    grid.addWidget(btn_search, 0, 4)
    grid.addWidget(plainText, 1, 0, 1, 5)
    window.setLayout(grid)

    app.exec_()
