import sys 
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *  
# Creating the main window 
class App(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        self.title = 'PyQt5 - QTabWidget'
        self.left = 0
        self.top = 0
        self.width = 1024
        self.height = 768
        self.setWindowTitle(self.title) 
        self.setGeometry(self.left, self.top, self.width, self.height)
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        
        newAction = QAction("file", self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        # newAction.triggered.connect(self.newCall)
        fileMenu.addAction(newAction) 
        # self.tab_widget = MyTabWidget(self) 
        # self.toolbar = QToolBar("My main toolbar")
        # self.addToolBar(self.toolbar)
        # button_action = QAction("Your button", self)
        # button_action.setStatusTip("This is your button")
        # self.setCentralWidget(self.tab_widget)
        self.layout = QVBoxLayout(self) 
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda index: self.demofunction(index)) 
        self.tab1 = QWidget() 
        self.tab2 = QWidget() 
        self.tab3 = QWidget() 
        self.tabs.resize(1024, 768) 
  
        # Add tabs 
        self.tabs.addTab(self.tab1, "Tab1") 
        self.tabs.addTab(self.tab2, "Tab2") 
        self.tabs.addTab(self.tab3, "Tab3") 

  
        # Create first tab 
        self.tab1.layout = QVBoxLayout(self) 
        self.l = QLabel() 
        self.l.setText("This is the first tab") 
        self.tab1.layout.addWidget(self.l) 
        self.tab1.setLayout(self.tab1.layout)
        # self.tab1.clicked.connect(self.demofunction) 
  
        # Create second tab
        self.tab2.layout = QVBoxLayout(self) 
        self.l = QLabel() 
        self.l.setText("This is the second tab") 
        self.tab2.layout.addWidget(self.l) 
        self.tab2.setLayout(self.tab2.layout)
        

        # Create third tab
        self.tab3.layout = QVBoxLayout(self) 
        self.l = QLabel() 
        self.l.setText("This is the third tab") 
        self.tab3.layout.addWidget(self.l) 
        self.tab3.setLayout(self.tab3.layout)
        self.show()
        
        # Add tabs to widget 
        # self.layout.addWidget(self.tabs) 
        # self.setLayout(self.layout)

    def demofunction(self,index):
        self.tabs.removeTab(index);
        # delete tabWidget_->widget(index);
        print("pass",index)  
        self.show() 
  
# Creating tab widgets 
class MyTabWidget(QWidget): 
    def __init__(self, parent): 
        super(QWidget, self).__init__(parent) 
        self.layout = QVBoxLayout(self) 
  
        # Initialize tab screen 
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda index: self.demofunction(index)) 
        self.tab1 = QWidget() 
        self.tab2 = QWidget() 
        self.tab3 = QWidget() 
        self.tabs.resize(1024, 768) 
  
        # Add tabs 
        self.tabs.addTab(self.tab1, "Tab1") 
        self.tabs.addTab(self.tab2, "Tab2") 
        self.tabs.addTab(self.tab3, "Tab3") 

  
        # Create first tab 
        self.tab1.layout = QVBoxLayout(self) 
        self.l = QLabel() 
        self.l.setText("This is the first tab") 
        self.tab1.layout.addWidget(self.l) 
        self.tab1.setLayout(self.tab1.layout)
        # self.tab1.clicked.connect(self.demofunction) 
  
        # Create second tab
        self.tab2.layout = QVBoxLayout(self) 
        self.l = QLabel() 
        self.l.setText("This is the second tab") 
        self.tab2.layout.addWidget(self.l) 
        self.tab2.setLayout(self.tab2.layout)
        

        # Create third tab
        self.tab3.layout = QVBoxLayout(self) 
        self.l = QLabel() 
        self.l.setText("This is the third tab") 
        self.tab3.layout.addWidget(self.l) 
        self.tab3.setLayout(self.tab3.layout)
        
        # Add tabs to widget 
        self.layout.addWidget(self.tabs) 
        self.setLayout(self.layout)

    def demofunction(self,index):
        self.tabs.removeTab(index);
        # delete tabWidget_->widget(index);
        print("pass",index) 
  
if __name__ == '__main__': 
    app = QApplication(sys.argv) 
    ex = App() 
    sys.exit(app.exec_()) 