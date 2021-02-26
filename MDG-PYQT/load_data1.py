from PyQt5 import QtCore, QtGui, QtWidgets
from helper import guess_data_types,clean_headers,enforce_data_types
from change_type import Ui_TypeWindow
import pandas as pd
from helper import show_error_message,show_success_message,engine,MySplashScreen
import sqlite3
from dateutil.parser import parse
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from loader import popup1
import asyncio
import pprint
import sip


class LoadThread(QtCore.QThread):
    signal = QtCore.pyqtSignal()

    def __init__(self,data,db_name,meta_data,main_window,db_function,splash):
        QtCore.QThread.__init__(self)
        self.data = data
        self.db_name = db_name
        self.meta_data = meta_data
        self.main_window = main_window
        self.splash = splash
        self.db_function = db_function

    # run method gets called when we start the thread
    def run(self):
        self.data = enforce_data_types(self.data,self.meta_data)
        print('NOW SAVINg')
        try:
            # save the database to the sqlite3
            self.data.to_sql(self.db_name,engine,if_exists='replace',index=False)
            # save the databasename column in the data frame

        except Exception as e:
                print(e)        
        meta_data_frame = pd.DataFrame(columns=['field','data_type','unique_data'])
        # fill the data frame from meta data dict
        for key in self.meta_data.keys():
            if self.meta_data[key]['datatype'] == 'CHARACTER':
                    char = ''
                    for d in self.data[key].unique():
                        char+=str(d)
                        char+='###'
                    meta_data_frame.loc[len(meta_data_frame)] = [key ,self.meta_data[key]['datatype'],char]
            else:
                meta_data_frame.loc[len(meta_data_frame)] = [key ,self.meta_data[key]['datatype'],f'''{self.data[key].min()},{self.data[key].max()}''']
        meta_data_frame['dbname']=self.db_name
        #save the dataset to database
        meta_data_frame.to_sql('meta_data',engine,if_exists='append')
        self.signal.emit()

class Data():
    list_type=[]
    column_name=[]
class FilterHeader(QHeaderView):
    filterActivated = pyqtSignal()

    def __init__(self, parent,meta_data=None):
        super().__init__(Qt.Horizontal, parent)
        self._editors = []
        self.list=[]
        self.list1=[]
        self.list2=[]
        self.label_dct = {}
        self._padding = 20
        self.meta_data = meta_data
        self.column_name_list=Data.column_name
        print("this is second meta data", meta_data)
        self.list_type=Data.list_type
        # self.setStretchLastSection(True)
        # self.setResizeMode(QHeaderView.Stretch)
        self.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setSortIndicatorShown(False)
        self.sectionResized.connect(self.adjustPositions)
        parent.horizontalScrollBar().valueChanged.connect(self.adjustPositions)

    def setFilterBoxes(self, count):
        while self._editors:
            editor = self._editors.pop()
            editor.deleteLater()
        for index in range(count):
            editor = self.create_editor(self.parent(), index,self.list_type[index])
            self._editors.append(editor)
        self.adjustPositions()

    def create_editor(self, parent, index,type):
        layout = QGridLayout()
        mapper = QSignalMapper(self)
        mapper1 = QSignalMapper(self)
        mapper2 = QSignalMapper(self)
        self.funlist=QListWidget()
        editor = QWidget(parent)
        editor.setLayout(layout)
        editor.setGeometry(0, 0, 0, 100)
        # editor.setStyleSheet("background-color:white;")
        editor.setStyleSheet("""

            QWidget{
            background-color:#F8F8F8;
            color:black;
            }
            
            QPushButton[Test=true] {
                border: 2px solid #8f8f91;
                border-radius: 6px;
                color: black;
                background-color: #DFDFDF;
                min-width: 80px;
            }

            QPushButton#StyledButton[Test=true] {
                color: #F00;
                background-color: #000;
            }
                           """
                           )
        editor.show()
        self.d_off = QPushButton('#')
        self.d_off.setProperty('Test', True)
        self.d_off.setCheckable(True)
        self.d_off.resize(1024, 768)
        self.list.append(self.d_off)
        self.d_off.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        itemN = QListWidgetItem()
        # Create widget
        widget = QWidget()
        widgetText = QLabel("I love PyQt!")
        widgetButton = QPushButton("Push Me")
        widgetLayout = QHBoxLayout()
        widgetLayout.addWidget(widgetText)
        widgetLayout.addWidget(widgetButton)
        widgetLayout.addStretch()

        widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
        widget.setLayout(widgetLayout)
        itemN.setSizeHint(widget.sizeHint())
        self.funlist.addItem(itemN)
        self.funlist.setItemWidget(itemN, widget)
        # pprint.pprint(vars(QPushButton))
        # pprint(pprintself.d_off
        self.d_off.clicked.connect(mapper.map)
        # QListWidgetItem(self.d_off)
        # mylistWidget.addItem(self.d_off)
        mapper.setMapping(self.d_off,index)
        mapper.mapped[int].connect(self.a_function)
        # self.d_off.clicked.connect(lambda: self.toggle(self.d_off),mapper)
        # self.d_off.setStyleSheet("QPushButton{background-color:#7B7B7B; color: white;border: none;border-style: outset;border-width:1px;border-radius: 1px;border-color: black;} QPushButton:checked { background-color:#4299ff;color:white; }")
        self.d_off.setChecked(True)
        
        self.d_50 = QPushButton('ABC', editor)
        self.d_50 .setProperty('Test', True)
        self.d_50.setCheckable(True)
        self.d_50.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.d_50.clicked.connect(mapper1.map)
        # QListWidgetItem(self.d_off)
        # mylistWidget.addItem(self.d_off)
        mapper1.setMapping(self.d_50,index)
        mapper1.mapped[int].connect(self.b_function)
        self.list1.append(self.d_50)
        # self.d_50.clicked.connect(lambda: self.toggle(self.d_50))
        # self.d_50.clicked.connect(self.creating_function)
        # self.d_50.setStyleSheet("QPushButton{background-color:#7B7B7B; color: white;border: none;border-style: outset;border-width:1px;border-radius: 1px;border-color: black;} QPushButton:checked { background-color:#4299ff;color:white; }")
        # pybutton.setChecked(True)
        self.d_100 = QPushButton('DATE', editor)
        self.d_100 .setProperty('Test', True)
        self.d_100.setCheckable(True)
        self.d_100.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.d_100.clicked.connect(mapper2.map)
        # self.d_100.clicked.connect(lambda d100:self.d_100_on(d100))
        # self.d_100.setStyleSheet("QPushButton{background-color:#7B7B7B; color: white;border: none;border-style: outset;border-width:1px;border-radius: 1px;border-color: black;} QPushButton:checked { background-color:#4299ff;color:white; }")
        self.list2.append(self.d_100)
        mapper2.setMapping(self.d_100,index)
        mapper2.mapped[int].connect(self.c_function)
        
        # self.label_dct[assign_button] = worker_label
        layout.addWidget(self.d_off)
        layout.addWidget(self.d_50)
        layout.addWidget(self.d_100)
        self.check(type,index)

        return editor
    def check(self,type,x):
        print("pass",type)
        if(type=="NUMBER"):
            self.list[x].setStyleSheet('background-color:#4299ff;color:white;')
        elif(type=="CHARACTER"):
            self.list1[x].setStyleSheet('background-color:#4299ff;color:white;')
        else:
            self.list2[x].setStyleSheet('background-color:#4299ff;color:white;')

    def a_function(self,x):

        print("x : ",x)
        print(self.d_off)
        # pprint.pprint(vars(QListWidget))
        print(self.funlist,self.list)
        var=self.column_name_list[x]
        self.meta_data[var]['datatype'] = "NUMBER"
        self.list[x].setStyleSheet('background-color:#4299ff;color:white;')
        self.list1[x].setStyleSheet('color: black;background-color: #DFDFDF;')
        self.list2[x].setStyleSheet('color: black;background-color: #DFDFDF;')
        # if(x==0):s
        #     self.list[0].setStyleSheet('background-color:green')

    def b_function(self,x):

        print("x : ",x)
        print(self.d_off)
        # pprint.pprint(vars(QListWidget))
        print(self.funlist,self.list)
        var=self.column_name_list[x]
        self.meta_data[var]['datatype'] = "CHARACTER"
        # self.list[x].setStyleSheet('background-color:red')
        self.list1[x].setStyleSheet('background-color:#4299ff;color:white;')
        self.list[x].setStyleSheet('color: black;background-color: #DFDFDF;')
        self.list2[x].setStyleSheet('color: black;background-color: #DFDFDF;')
        # if(x==0):
        #     self.list[0].setStyleSheet('background-color:red')
    def c_function(self,x):

        print("x : ",x)
        print(self.d_off)
        # pprint.pprint(vars(QListWidget))
        print(self.funlist,self.list)
        var=self.column_name_list[x]
        self.meta_data[var]['datatype'] = "DATE"
        # self.list[x].setStyleSheet('background-color:red')
        self.list2[x].setStyleSheet('background-color:#4299ff;color:white;')
        self.list1[x].setStyleSheet('color: black;background-color: #DFDFDF;')
        self.list[x].setStyleSheet('color: black;background-color: #DFDFDF;')
        # if(x==0):
        #     self.list[0].setStyleSheet('background-color:red')
    def creating_function(self):
        nbtn = self.sender()
        pprint.pprint(vars(nbtn))
        print(nbtn.text())
        if(nbtn.text()=="ABC"):
            self.d_off.setEnabled(True)
            self.d_50.setEnabled(False)
            self.d_100.setEnabled(True)
            
            self.d_off.setCheckable(False)
            self.d_off.setEnabled(False)
            self.d_off.setEnabled(True)
            self.d_off.setCheckable(True)

            self.d_100.setCheckable(False)
            self.d_100.setEnabled(False)
            self.d_100.setEnabled(True)
            self.d_100.setCheckable(True)


    def sizeHint(self):
        size = super().sizeHint()
        if self._editors:
            height = self._editors[0].sizeHint().height()
            size.setHeight(size.height() + height + self._padding)
        return size

    def updateGeometries(self):
        if self._editors:
            height = self._editors[0].sizeHint().height()
            self.setViewportMargins(0, 0, 0, height + self._padding)
        else:
            self.setViewportMargins(0, 0, 0, 0)
        super().updateGeometries()
        self.adjustPositions()

    def adjustPositions(self):
        for index, editor in enumerate(self._editors):
            if not isinstance(editor, QWidget):
                continue
            height = editor.sizeHint().height()
            compensate_y = 0
            compensate_x = 0
            if type(editor) is QComboBox:
                compensate_y = +2
            # elif type(editor) in (QWidget, Widget):
            #     compensate_y = -1
            elif type(editor) is QPushButton:
                compensate_y = -1
            elif type(editor) is QCheckBox:
                compensate_y = 4
                compensate_x = 4
            editor.move(
                self.sectionPosition(index) - self.offset() + 1 + compensate_x,
                36+ compensate_y,
            )
            editor.resize(self.sectionSize(index), height+5)

    def filterText(self, index):
        for editor in self._editors:
            if hasattr(editor, "text") and callable(editor.text):
                return editor.text()
        return ""

    def setFilterText(self, index, text):
        for editor in self._editors:
            if hasattr(editor, "setText") and callable(editor.setText):
                editor.setText(text)

    def clearFilters(self):
        for editor in self._editors:
            editor.clear()
class Ui_Select1(object):
    
    def __init__(self,data=None,dropdown=None,db_function=None,temp_widget=None,temp_layout=None,mfunction=None,use_datasource_button=None,db_name=None):
        super().__init__()
        Data.list_type.clear()
        Data.column_name.clear()

        self.temp_widget = temp_widget
        self.temp_layout = temp_layout
        self.mfunction = mfunction
        self.create_graphs_function = use_datasource_button
        self.db_name = db_name
        # get the dropdown menu from the previous window
        self.comboBox = dropdown
        # get the function from the previous window
        self.db_function = db_function
        # clean the data helder from the function imported from data
        self.data = clean_headers(data)
        # get the data columns in string format
        self.data_columns = [str(d) for d in self.data.columns.values]
        # create a list of the data types that a dataframe has
        self.guess_types = guess_data_types(self.data)
        #creataa dictionary with data types
        self.meta_data = self.process_meta_data()
        print(self.meta_data,"this is meta data")
        self.text=""

    def setupUi(self, Select):
        # set object name of the  main window which is names as select
        Select.setObjectName("Select")
        # resize the window 
        # Select.resize(1024, 768)
        
        
        # Select.setMinimumSize(1024, 768)
        Select.showMaximized()

        self.layout = QVBoxLayout()

        Select.setLayout(self.layout) 
        # set the central widget in main window
        self.centralwidget = QtWidgets.QWidget(Select)
        # self.centralwidget.setStyleSheet('background-color:red')
        # self.centralwidget.setFixedSize(768, 768)
        self.layout.addWidget(self.centralwidget)
        # set the object name
        self.centralwidget.setObjectName("centralwidget")
        # create a qtable widget 
        # self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        # set the position of widget
        # self.tableWidget.setGeometry(QtCore.QRect(10, 70, 731, 192))
        # set the obejct name of the tablewidget
        # self.tableWidget.setObjectName("tableWidget")
        # intitliaze the column count
        # self.tableWidget.setColumnCount(0)
        # intitliizie the row count
        # self.tableWidget.setRowCount(0)
        # add a text field
        print("Slect width",Select.width())
        # self.plainTextEdit = QtWidgets.QLineEdit(self.centralwidget)
        # self.plainTextEdit.textChanged.connect(self.textchanged)
        # self.plainTextEdit.setFixedWidth(int(Select.width()/2))
        # # self.plainTextEdit.setGeometry(QtCore.QRect(10, 320, 171, 31))
        # self.plainTextEdit.setObjectName("plainTextEdit")
        # add alabel widgetr
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 300, 131, 16))
        self.label.setObjectName("label")
        self.label.setText(self.db_name)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont('Arial')
        font.setPixelSize(17)
        self.label.setFont(font)
        # add a pusgh button
        #self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton = QtWidgets.QPushButton(None)
        # self.pushButton.setFixedSize(111, 41)
        self.pushButton.setStyleSheet('''       
        QPushButton
        {
            padding-top:10px;padding-bottom:10px;padding-left:30px;padding-right:30px;
            border-radius: 5px;
            color: black;
            background-color: #DFDFDF;
        }

        QPushButton::disabled
        {
            color: #acacac;
        }

        QPushButton:hover
        {
            background: #6e98e0;
            color: white;
            
        }

        QPushButton:pressed
        {padding-top:10px;padding-bottom:10px;padding-left:30px;padding-right:30px;
        background: #6e98e0;
            color: white;

        }
        QPushButton:checked
        {
        padding-top:10px;padding-bottom:10px;padding-left:30px;padding-right:30px;
background: #6e98e0;
            color: white;
        }''')
        # self.pushButton.setGeometry(QtCore.QRect(320, 430, 111, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda:self.save_dataset(Select))
        # self.label_2 = QtWidgets.QLabel(self.centralwidget)
        # self.label_2.setGeometry(QtCore.QRect(10, 30, 151, 21))
        # font = QtGui.QFont()
        # font.setPointSize(20)
        # self.label_2.setFont(font)
        # self.label_2.setObjectName("label_2")
        # Select.setCentralWidget(self.centralwidget)
        
        # self.statusbar = QtWidgets.QStatusBar(Select)
        # self.statusbar.setObjectName("statusbar")
        
        # Select.setStatusBar(self.statusbar)

        # self.create_graphs = QPushButton("Use Datasource")
        # self.create_graphs.setFixedSize(150, 34)
        # self.create_graphs.setFont(QFont('Arial',13))
        # self.create_graphs.setStyleSheet(
        # '''
        # QPushButton
        # {
        #     color: white;
        #     background-color:#327EFF;
        #     border: 1.5px solid #327EFF;

        # }
        # QPushButton:hover
        # {
        #     background: #6e98e0;
        #     color: white;
            
        # }'''
            
        #     )
        # self.create_graphs.clicked.connect(self.create_graphs_function)

        self.retranslateUi(Select)
        QtCore.QMetaObject.connectSlotsByName(Select)
        # self.tableWidget.horizontalHeader().sectionClicked.connect(self.clicked_column)

        self.filter_button = QPushButton("Filter")
        self.filter_button.setCheckable(True)
        self.filter_button.setChecked(True)
        self.filter_button.clicked.connect(self.on_button_clicked)
        
        self.view = QTableView()
        self.view.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        # self.view.setAttribute(Qt.AA_DisableHighDpiScaling)
        # self.view.setHorizontalStretch(0);
        # self.view.setVerticalStretch(0);
        # self.view.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        font = QFont('Arial')
        font.setPixelSize(13)
        self.view.setFont(font)
        self.view.setStyleSheet('''
        QHeaderView::section{Background-color:#F8F8F8;
        color:black;
    border: 1px solid rgb(153, 153, 153);
    border-width: 1px 1px 1px 1px;
    padding-left:8px;
    }
            '''
            )
        # self.view.horizontalHeader().setStretchLastSection(True)

        button_layout = QHBoxLayout()
        #button_layout.addWidget(self.pushButton)
        button_layout.addStretch(1)
        # button_layout.addWidget(self.create_graphs)

        layout = QVBoxLayout(self.centralwidget)
        # layout.addWidget(self.label_2)
        layout.addWidget(self.label)
        # layout.addWidget(self.plainTextEdit)
        layout.addLayout(button_layout)
        # layout.addWidget(self.pushButton)
        layout.addWidget(self.view)
        print(self.meta_data,"this is meta data")


    def textchanged(self,text):
        print(text)
        # print "contents of text box: "+text
        self.text=text

    def handleFilterActivated(self):
        header = self.view.horizontalHeader()
        # print()
        for index in range(header.count()):
            if index != 4:
                print(index, header.filterText(index))
            else:
                print("Button")

    def on_button_clicked(self):
        if self.filter_button.isChecked():
            QMessageBox.information(None, "", "Now I want the row with filters below the QHeaderView to appear again.")
        else:
            QMessageBox.information(None, "", "Now I want the row with filters below the QHeaderView to disappear.")


    def clicked_column(self,logical_index):
        '''
            This function open the  datattype dialigue to change the datatype
        '''
        # get the columns name of the data
        column_name = self.data_columns
        print(column_name[logical_index])
        # geet the cslected the column
        current = self.guess_types[column_name[logical_index]]
        print(current['datatype'])
        # passs it into change data type window
        self.Select = QtWidgets.QMainWindow()
        self.ui = Ui_TypeWindow(current['datatype'],column_name[logical_index],self.meta_data)
        self.ui.setupUi(self.Select)
        self.ui.set_dropdown_options()
        self.Select.show()

    def process_meta_data(self):
        '''
            create a dict with the guessed data columns
        '''
        meta_data ={}
        for column in self.data_columns:
            meta_data[column] = {}
            meta_data[column]['datatype'] = self.guess_types[column]['datatype']
        return meta_data

    def save_dataset(self,main_window):
        db_name=self.text
        if db_name == '':
            show_error_message('Please Enter dataset Name')
        else:
            # disable the button
            self.pushButton.setEnabled(False)
            #replace the space with the underscore
            try:
                db_name = db_name.replace(' ','_')
            except:
                pass
        print('##############################################')
        self.splash = MySplashScreen(QtGui.QPixmap('logo1.png'))       
        self.thread = LoadThread(self.data,db_name,self.meta_data,main_window,self.db_function,self.splash)
        self.thread.signal.connect(lambda:self.thread_finished(db_name))
        self.thread.start()
        self.splash.show()

    def thread_finished(self,db_name):
        self.splash.close()
        show_success_message('Successfully dataset Loaded.')
        self.db_function()
        sip.delete(self.temp_widget )
        self.widget2_1 = QWidget()
        self.widget2_1.setStyleSheet("background:#F8F8F8")
        self.widget2_1.setVisible(True)
        self.temp_layout.addWidget(self.widget2_1,1,1)
        self.passvalue = db_name
        self.mfunction(self.widget2_1,self.passvalue) 
            # get_all_database


    # def csv_to_sqlite(self,df,db_name):
    #     result = []
    #     data = df[:1]
    #     data.to_sql(db_name,engine,if_exists='replace',index=False)
    #     for i in range(len(df)):
    #         result.extend(list(df.loc[i].values))
    #     print(result)
    #     conn = sqlite3.connect("sqlite.db")
    #     c = conn.cursor()
    #     str_1 = ''
    #     for i in range(len(self.data_columns)):
    #         if i == len(self.data_columns) -1:
    #             str_1 += '?'
    #         else:
    #             str_1 += '?,'
    #     # sql_query = 
    #     # print(sql_query)
    #     c.executemany('insert into asd values (?,?,?,?)', result)
    #     conn.commit()
    #     conn.close()

    def fill_table(self):
        '''
            fill the table with data 
        '''
        #get 10 rows of data
        temp_list=[]
        # print(str(self.data.columns.tolist()),"this is columns")
        # print("all_data",self.data)
        all_data = self.data[:20]
        temp_list.append(all_data)
        pprint.pprint(vars(all_data))



        column_name = self.data_columns
        print(column_name[0])
        # # geet the cslected the column
        for names in column_name:
            current = self.guess_types[names]
            print(current['datatype'])
            Data.list_type.append(current['datatype'])
        
        print(Data.list_type)
        Data.column_name=self.data.columns.tolist()
        header = FilterHeader(self.view,self.meta_data)
        # self.view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed);
        # self.view.verticalHeader().setDefaultSectionSize(24);
        self.view.setHorizontalHeader(header)
        self.view.verticalHeader().setVisible(False)
        # self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);
        # self.view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # print("checking")
        # self.tableWidget.setColumnCount(len(self.data_columns))
        # self.tableWidget.setRowCount(10)
        #model = QStandardItemModel(self.view)
        print("this is data columns",self.data_columns)
        model = QStandardItemModel(10,len(self.data_columns),self.view)
        print(all_data,"this is all_data")
        for key,value in all_data.items():
            for k,val in enumerate(value):
                item = QStandardItem(str(val))
                model.setItem(k,self.data_columns.index(key),item)
        showHeader=""
        for item1 in self.data.columns.tolist():
            showHeader=showHeader+" "+item1
        print(showHeader)
        Data.column_name=self.data.columns.tolist()
        model.setHorizontalHeaderLabels(str(showHeader).split())
        self.view.setModel(model)
        header.setFilterBoxes(model.columnCount())
        header.filterActivated.connect(self.handleFilterActivated)
        # self.model = TableModel(all_data)
        # self.view.setModel(self.model)
        # set the column count 
        # self.tableWidget.setColumnCount(len(self.data_columns))
        # set row count
        # self.tableWidget.setRowCount(10)
        #set data column labels
        # self.tableWidget.setHorizontalHeaderLabels(self.data.columns)
        # iterate over the data and set it into table
        # for key,value in all_data.items():
            # for k,val in enumerate(value):
                # self.tableWidget.setItem(k,self.data_columns.index(key),QtWidgets.QTableWidgetItem(str(val)))
        
    def retranslateUi(self, Select):
        _translate = QtCore.QCoreApplication.translate
        Select.setWindowTitle(_translate("Select", "MainWindow"))
        # self.label.setText(_translate("Select", "Enter Datasource Name"))
        #self.pushButton.setText(_translate("Select", "Update Data"))
        # self.label_2.setText(_translate("Select", "Load Data"))