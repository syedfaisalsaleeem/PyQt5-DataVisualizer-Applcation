import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
class popup1(QDialog):
    def __init__(self,index=None,tabwidget=None):
        super().__init__()
        self.title = "App"
        self.index=index
        self.tabwidget=tabwidget
        self.text=""
        #self.tablefirsttime=0
        self.InitUI()
    def InitUI(self):
            #a=QFrame()
            #print("start")
            screen = app.primaryScreen()
            size = screen.size()
            # MainWindow.resize(size.width()*80/100, size.height()*80/100)
            self.resize(int(size.width()*25/100),int(size.height()*18/100))
            self.setWindowModality(Qt.ApplicationModal)
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.setStyleSheet('background-color:white;')
            # self._gif =QLabel(self)
            # self._gif.move(215,30)
            # self._gif.setStyleSheet('background-color:white;border:0px solid white')
            # movie = QMovie("as4.gif")
            # self._gif.setMovie(movie)
            # movie.setSpeed(500)
            # movie.start()
            label1 = QLabel('Rename',self)
            label1.setFont(QFont('Arialbold', 20))
            label1.setStyleSheet('background-color:white;border:0px solid white')
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(label1)
            hbox.addStretch(1)
            
            label2 = QLabel("Are you sure you want to rename the tab ?",self)
            label2.setFont(QFont('Arial', 12))
            label2.setStyleSheet('background-color:white;border:0px solid white')
            hbox2 = QHBoxLayout()
            hbox2.addStretch(1)
            hbox2.addWidget(label2)
            hbox2.addStretch(1)
            
            label3 = QLabel("Name of tab:",self)
            label3.setFont(QFont('Arial', 12))
            label3.setStyleSheet('background-color:white;border:0px solid white')
            self.plainTextEdit = QtWidgets.QLineEdit(self)
            self.plainTextEdit.textChanged.connect(self.textchanged)
            # self.plainTextEdit.setFixedSize(200, 20)
            
            hbox3 = QHBoxLayout()
            hbox3.addStretch(1)
            hbox3.addWidget(label3)
            hbox3.addWidget(self.plainTextEdit)
            hbox3.addStretch(1)

            okButton = QPushButton("Yes")
            okButton.setFixedSize(150, 50)
            okButton.setFont(QFont('Arial', 12))
            okButton.setStyleSheet('background-color:#103F91;color:white')
            okButton.clicked.connect(self.call_yes)
            cancelButton = QPushButton("No")
            cancelButton.setFixedSize(150, 50)
            cancelButton.setFont(QFont('Arial', 12))
            cancelButton.setStyleSheet('background-color:#F22323;color:white')
            cancelButton.clicked.connect(self.call_no)
            
            hbox4 = QHBoxLayout()
            hbox4.addStretch(1)
            hbox4.addWidget(okButton)
            hbox4.addWidget(cancelButton)
            
            vbox = QVBoxLayout()
            # vbox.addStretch(1)
            vbox.addLayout(hbox)
            # vbox.addStretch(0.1)
            vbox.addLayout(hbox2)
            vbox.addStretch(1)
            vbox.addLayout(hbox3)
            vbox.addStretch(1)
            vbox.addLayout(hbox4)
            self.setLayout(vbox)
            # self.vbox=QVBoxLayout(self)
            # self.vbox.setAlignment(Qt.AlignCenter)
            # # self.vbox.addWidget(self.label)
            # self.setLayout(self.vbox)
            # self.hbox = QHBoxLayout(self)

            # label1.move(236,130)

            # label2.move(50,170)
            # self.vbox.addWidget(label1)
            # self.vbox.addStretch(1)
            # self.vbox.addWidget(label2)
            # self.plainTextEdit = QtWidgets.QLineEdit(self)
            # self.plainTextEdit.textChanged.connect(self.textchanged)
            # yes = QPushButton("no", self)
            # yes.setGeometry(155,240,240,80)
            # yes.setFont(QFont('Arial', 21))
            # yes.setStyleSheet('background-color:#4299ff; color: white')
            # yes.clicked.connect(self.call_yes)
            # no = QPushButton("no", self)
            # no.setGeometry(155,240,240,80)
            # no.setFont(QFont('Arial', 21))
            # no.setStyleSheet('background-color:#4299ff; color: white')
            # no.clicked.connect(self.call_no)
            #self.show()
            #a.show()
    def textchanged(self,text):
        print(text)
        # print "contents of text box: "+text
        self.text=text

    def call_yes(self):
        self.tabwidget.setTabText(self.index,self.text)
        self.close()

    def call_no(self):
        self.close()
        # self.tabwidget.setTabText(self.index,self.text)
        # self.close()
        #self.destroy()
        #gc.collect() 

class TabExample(QMainWindow):
    def __init__(self):
        super(TabExample, self).__init__()
        self.setWindowTitle("Tab example")

        # Create widgets
        self.tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Label's to fill widget
        self.label1 = QtWidgets.QLabel("Tab 1")
        self.label2 = QtWidgets.QLabel("Tab 2")

        # Adding tab's
        self.tab_widget.addTab(self.label1, "Tab 1")
        self.tab_widget.addTab(self.label2, "Tab 2")
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(lambda index: self.demofunction(index)) 
        self.tab_widget.tabBarDoubleClicked.connect(lambda index: self.rename_tab(index))

        # Tab button's
        # self.right = self.tab_widget.tabBar().LeftSide
        # self.tab_widget.tabBar().setTabButton(0, self.right, TabButtonWidget())
        # self.tab_widget.tabBar().setTabButton(1, self.right, TabButtonWidget())

        # Tab settings
        self.tab_widget.tabBar().setMovable(True)

        self.show()

    def rename_tab(self,index):
        self.x=popup1(index,self.tab_widget)
        self.x.show()
        print("pass",index)

    def demofunction(self,index):
        self.tab_widget.removeTab(index);
        # delete tabWidget_->widget(index);
        # self.tab_widget.setTabText(index,"faisal")
        print("pass",index)  
        # self.show() 

class TabButtonWidget(QtWidgets.QWidget):
    def __init__(self):
        super(TabButtonWidget, self).__init__()
        # Create button's
        self.button_add = QtWidgets.QPushButton("+")
        # self.button_remove = QtWidgets.QPushButton("-")

        # Set button size
        self.button_add.setFixedSize(16, 16)
        # self.button_remove.setFixedSize(16, 16)

        # Create layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Add button's to layout
        self.layout.addWidget(self.button_add)
        # self.layout.addWidget(self.button_remove)

        # Use layout in widget
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TabExample()
    sys.exit(app.exec_())