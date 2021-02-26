from PyQt5 import QtCore, QtGui, QtWidgets
from helper import show_error_message

class PopupFile(object):
    
    # create a constructor in to set data from the previous window we need 
    def __init__(self,sheet,text,func,filename):
        super().__init__()
        self.sheet = sheet
        self.text = text
        self.load_func = func
        self.filename = filename

    # sets up the UI we pass Mainwindow widget in the function
    def setupUi(self, MainWindow):
        #set name of the object of main window
        MainWindow.setObjectName("MainWindow")
        # set the size of the main window
        MainWindow.resize(500, 238)
        # creaete a central widget where all the widgets will come
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        #set name
        self.centralwidget.setObjectName("centralwidget")
        #create a label widget
        self.label = QtWidgets.QLabel(self.centralwidget)
        # place the label in the postion with x y axes and hight width
        self.label.setGeometry(QtCore.QRect(120, 50, 250, 20))
        # create a font object
        font = QtGui.QFont()
        # set the font size
        font.setPixelSize(15)
        # set the font in the label 
        self.label.setFont(font)
        # set the object name of the label
        self.label.setObjectName("label")
        self.label.setText(self.text)
        # create a dropdown it is named as comoboox
        self.comboBox1 = QtWidgets.QComboBox(self.centralwidget)
        # set the poistion of combobox 
        self.comboBox1.setGeometry(QtCore.QRect(150, 100, 150, 30))
        #set the obejct name of combox
        self.comboBox1.setObjectName("comboBox")
        # if current is not none then set the current value which we set in the constructor
        self.comboBox1.addItem('Choose ...')
        # create a button widget
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        # set the position of the widget
        self.pushButton.setGeometry(QtCore.QRect(175, 170, 100, 31))
        # set the object name 
        self.pushButton.setObjectName("pushButton")
        # set the event when button is pushed to execute the function
        self.pushButton.clicked.connect(lambda:self.change_data_type(MainWindow))
        #set main window centeral widget 
        MainWindow.setCentralWidget(self.centralwidget)
        # create a widget of the status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # set the object name
        self.statusbar.setObjectName("statusbar")
        # set status bar in the mmain window
        MainWindow.setStatusBar(self.statusbar)
        self.set_dropdown_options()
        # call retransalatre UI
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # set the title of the window
        MainWindow.setWindowTitle(_translate("MainWindow", "Vizpick"))
        # set the title of column name
        # set the button title
        self.pushButton.setText(_translate("MainWindow", "Select"))

    def change_data_type(self,main_window):
        ''' 
            This function is responsible to detect change in the 
            datatype and save it into meta data
        '''
    
        sheet = str(self.comboBox1.currentText())
        if sheet != 'Choose ...':
            if sheet == 'space':
                sheet = ' '
            #set the value of column with data type
            self.load_func(sheet,self.filename)
            # close the window
            main_window.close()
        else:
            show_error_message('Please select a option')
        

    def set_dropdown_options(self):
        ''' 
            This function is responsible for filling up the dropdown
        '''
        for c in self.sheet:
            self.comboBox1.addItem(c)

if __name__ == "__main__":
    import sys
    # intialized app in the with Qapplication
    app = QtWidgets.QApplication(sys.argv)
    # create a main window
    MainWindow = QtWidgets.QMainWindow()
    ui = PopupFile()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())