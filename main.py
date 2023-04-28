import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Example')
        self.setGeometry(100, 100, 400, 300)
        self.button = QPushButton('Click me!', self)
        self.button.setToolTip('This is a tooltip for the button.')
        self.button.move(150, 100)
        self.button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        print('The button was clicked!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
