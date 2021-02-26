from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class popup1(QDialog):
    def __init__(self,name=None,name2=None):
        super().__init__()
        self.title = "App"
        self.name=name
        self.name2=name2
        #self.tablefirsttime=0
        self.InitUI()
    def InitUI(self):
            #a=QFrame()
            #print("start")
            self.setGeometry(237,209,550,350)
            self.setWindowModality(Qt.ApplicationModal)
            self.setWindowFlags(Qt.WindowStaysOnTopHint  | Qt.FramelessWindowHint)
            self.setStyleSheet('background-color:white;border:2px solid black')
            self._gif =QLabel(self)
            self._gif.move(215,30)
            self._gif.setStyleSheet('background-color:white;border:0px solid white')
            movie = QMovie("as4.gif")
            self._gif.setMovie(movie)
            movie.setSpeed(500)
            movie.start()
            label1 = QLabel('Error',self)
            label1.setFont(QFont('Arialbold', 22))
            label1.setStyleSheet('background-color:white;border:0px solid white')
            label1.move(236,130)
            label2 = QLabel(self.name,self)
            label2.setFont(QFont('Arial', 19))
            label2.setStyleSheet('background-color:white;border:0px solid white')
            label2.move(50,170)
            no = QPushButton(self.name2, self)
            no.setGeometry(155,240,240,80)
            no.setFont(QFont('Arial', 21))
            no.setStyleSheet('background-color:#4299ff; color: white')
            no.clicked.connect(self.call_no)
            self.show()
            #a.show()
    def call_no(self):
        self.close()

# class Ui_MainWindow(object):
#     """docstring for Ui_MainWindow"""
#     def __init__(self):
#         super(Ui_MainWindow, self).__init__()
#         self.popup1=popup1("none","close")
#         self.popup1.show()
        
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     MainWindow = QMainWindow()
#     ui = Ui_MainWindow()
#     # ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
