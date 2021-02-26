import os
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from graph1011 import Graph1011
from helper import ExtendedTextBox, BoxStyle, run_query, data_label_decimal, data_label_format
from super_graph import SuperGraph
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import squarify
import helper
from data_format_round import DataLabelFormatter
from sklearn.linear_model import LinearRegression
from data_format_round import DataLabelFormatter
import circle as circ

BoxStyle._style_list["ext"] = ExtendedTextBox
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from TopBar import TopLearningSection
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import dateformater
from sklearn.linear_model import LinearRegression
class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mousePressEvent(self, event)


class Graph1111(SuperGraph):
    # constructor to intialize the variables
    def __init__(self, fields=None, prev_win=None, db_name=None, field_str=None, graph_class=None):
        SuperGraph.__init__(self)
        self.y_axis = 0
        self.fields = fields
        self.prev_win = prev_win
        self.db_name = db_name
        self.field_str = field_str
        self.graph_class = graph_class

    def setupUi(self, MainWindow):
        # close the previous window
        # self.prev_win.hide()
        self.main_window_layout = QVBoxLayout()
        self.main_window = MainWindow
        self.t = TopLearningSection()
        self.t.setup(self.main_window_layout )
        self.main_window_layout.setAlignment(Qt.AlignTop)
        # self.vbox.addLayout(self.hbox1)
        # self.vbox.addLayout(self.hbox)
        self.main_window.setLayout(self.main_window_layout)
        # self.centralwidget = MainWindow#QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setObjectName("centralwidget")

        ## Adding top widget without scroll area
        self.fixedwidgettop = QWidget()
        self.fixedwidgettop.setStyleSheet('background:white')
        self.effect = QGraphicsDropShadowEffect(self.fixedwidgettop)
        self.effect.setOffset(0, 0)
        self.effect.setBlurRadius(10)
        self.fixedwidgettop.setGraphicsEffect(self.effect)
        self.fixedwidgettop.setFixedHeight(250)

        # THis is the main horizontal layout inside  fixed widget at the top
        self.hlayoutfixedwidgettop = QHBoxLayout()
        self.hlayoutfixedwidgettop.setAlignment(Qt.AlignTop)

        self.smallwidgetinsidefixedwidgettop = QWidget()
        self.smallwidgetinsidefixedwidgettop.setStyleSheet("background:white")
        self.smallwidgetinsidefixedwidgettop.setFixedSize(1250, 240)

        # Adding vertical layouts 4 columns inside small widget at top
        self.vlayoutfixedwidgettop = QVBoxLayout()
        self.vlayoutfixedwidgettop.setAlignment(Qt.AlignCenter)
        # self.vlayoutfixedwidgettop.setAlignment(Qt.AlignTop)
        self.smallwidgetinsidefixedwidgettop.setLayout(self.vlayoutfixedwidgettop)
        # self.smallwidgetinsidefixedwidgettop.setMinimumWidth(600)
        self.hlayoutfixedwidgettop.addStretch(1)
        self.hlayoutfixedwidgettop.addWidget(self.smallwidgetinsidefixedwidgettop)
        self.hlayoutfixedwidgettop.addStretch(1)
        self.fixedwidgettop.setLayout(self.hlayoutfixedwidgettop)

        self.hboxwidgetinsiderow3 = QHBoxLayout()
        self.hboxwidgetinsiderow3.setAlignment(Qt.AlignLeft)
        self.button3 = QWidget(self.smallwidgetinsidefixedwidgettop)
        self.button3.setFixedWidth(1250)

        self.button3.setLayout(self.hboxwidgetinsiderow3)
        self.pushButton_2 = QtWidgets.QPushButton(self.button3)
        self.pushButton_2.setStyleSheet('''
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
            }
                ''')
        # self.pushButton_2.setGeometry(QtCore.QRect(10, 10, 150, 50))
        self.pushButton_2.setFixedSize(150, 40)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText('Filter')
        self.pushButton_2.clicked.connect(self.open_filter)
        # self.vlayoutfixedwidgettop.addWidget(self.pushButton_2)

        ##Adding scrollablewidget with scrollarea

        self.main_window_layout.addWidget(self.fixedwidgettop)
        # self.mainwidget.setLayout(self.mainlayout)
        self.create_area(MainWindow, MainWindow.width(), MainWindow.height(), self.main_window_layout,
                         self.fixedwidgettop, self.vlayoutfixedwidgettop, self.pushButton_2,
                         self.smallwidgetinsidefixedwidgettop)

        self.get_data_from_table()

        self.run_spinner()
        # self.generate_graph(self.fields,self.y_axis,self.field_str)
        self.generate_top_text()
        self.vlayoutfixedwidgettop.addWidget(self.button3)
        self.hboxwidgetinsiderow3.addWidget(self.pushButton_2)
        self.generate_category_button()

        self.vlayoutfixedwidgettop.addStretch(1)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # def create_tab(self,tab_label):
    #     self.tab_2 = QtWidgets.QWidget()
    #     self.tab_2.setObjectName("tab_2")
    #     self.tabWidget.addTab(self.tab_2, "")
    #     self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),tab_label)

    def create_sql_queries(self, flag=False, where_func=False):
        data = []
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]

        if flag:
            where_filters = where_func
        else:
            where_filters = ''
        where_sql = ''
        if self.fields['aggregate'][0] == 'Sum':
            if self.fields['date_level'][0] == 'Exact Date':
                min_max_sql = f'''select min(date({date_selection})) as min_date_level, max(date({date_selection})) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}) as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}), {character_selection}'''
                order_sql = f''' order by date({date_selection}), coalesce(sum({number_selection}),0) desc'''
            elif self.fields['date_level'][0] == 'Week':
                min_max_sql = f'''select min(date({date_selection}, 'weekday 1', '-7 days')) as min_date_level, max(date({date_selection}, 'weekday 1', '-7 days')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'weekday 1', '-7 days') as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'weekday 1', '-7 days'), {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'weekday 1', '-7 days'), coalesce(sum({number_selection}),0) desc'''
            elif self.fields['date_level'][0] == 'Month':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of month') as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of month'), {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'start of month'), coalesce(sum({number_selection}),0) desc'''
            elif self.fields['date_level'][0] == 'Quarter':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END), {character_selection}'''
                order_sql = f''' order by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END), coalesce(sum({number_selection}),0) desc'''
            elif self.fields['date_level'][0] == 'Year':
                min_max_sql = f'''select min(date({date_selection}, 'start of year')) as min_date_level, max(date({date_selection}, 'start of year')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of year') as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of year'), {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'start of year'), coalesce(sum({number_selection}),0) desc'''
            if where_filters != '':
                where_sql += ' where ' + where_filters
            else:
                where_filters += ''

            sql_statement = select_sql + where_sql + group_sql + order_sql

        elif self.fields['aggregate'][0] == 'Average':
            if self.fields['date_level'][0] == 'Exact Date':
                min_max_sql = f'''select min(date({date_selection})) as min_date_level, max(date({date_selection})) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}) as {date_selection},  {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}),  {character_selection}'''
                order_sql = f''' order by date({date_selection}), avg({number_selection}) desc'''
            elif self.fields['date_level'][0] == 'Week':
                min_max_sql = f'''select min(date({date_selection}, 'weekday 1', '-7 days')) as min_date_level, max(date({date_selection}, 'weekday 1', '-7 days')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'weekday 1', '-7 days') as {date_selection}, {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'weekday 1', '-7 days'),  {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'weekday 1', '-7 days'), avg({number_selection}) desc'''
            elif self.fields['date_level'][0] == 'Month':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of month') as {date_selection}, {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of month'),  {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'start of month'), avg({number_selection}) desc'''
            elif self.fields['date_level'][0] == 'Quarter':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END as {date_selection}, {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END), {character_selection}'''
                order_sql = f''' order by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END), coalesce(sum({number_selection}),0) desc'''
            elif self.fields['date_level'][0] == 'Year':
                min_max_sql = f'''select min(date({date_selection}, 'start of year')) as min_date_level, max(date({date_selection}, 'start of year')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of year') as {date_selection}, {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of year'),  {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'start of year'), avg({number_selection}) desc'''
            if where_filters != '':
                where_sql += ' where ' + where_filters
            else:
                where_filters += ''

            sql_statement = select_sql + where_sql + group_sql + order_sql

        elif self.fields['aggregate'][0] == 'Count':
            if self.fields['date_level'][0] == 'Exact Date':
                min_max_sql = f'''select min(date({date_selection})) as min_date_level, max(date({date_selection})) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}) as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}),  {character_selection}'''
                order_sql = f''' order by date({date_selection}), count(*) desc'''
            elif self.fields['date_level'][0] == 'Week':
                min_max_sql = f'''select min(date({date_selection}, 'weekday 1', '-7 days')) as min_date_level, max(date({date_selection}, 'weekday 1', '-7 days')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'weekday 1', '-7 days') as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'weekday 1', '-7 days'),  {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'weekday 1', '-7 days'), count(*) desc'''
            elif self.fields['date_level'][0] == 'Month':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of month') as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of month'),  {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'start of month'), count(*) desc'''
            elif self.fields['date_level'][0] == 'Quarter':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END), {character_selection}'''
                order_sql = f''' order by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END), coalesce(sum({number_selection}),0) desc'''
            elif self.fields['date_level'][0] == 'Year':
                min_max_sql = f'''select min(date({date_selection}, 'start of year')) as min_date_level, max(date({date_selection}, 'start of year')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of year') as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of year'),  {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'start of year'), count(*) desc'''
            if where_filters != '':
                where_sql += ' where ' + where_filters
            else:
                where_filters += ''

            sql_statement = select_sql + where_sql + group_sql + order_sql
        print(sql_statement)
        df = run_query(sql_statement)
        data.append(df)

        #query 2
        if flag:
            where_filters = where_func
        else:
            where_filters = ''
        where_sql = ''
        if self.fields['aggregate'][0] == 'Sum':
            if self.fields['date_level'][0] == 'Exact Date':
                min_max_sql = f'''select min(date({date_selection})) as min_date_level, max(date({date_selection})) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}) as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}), {character_selection}'''
                order_sql = f''' order by date({date_selection}) desc, coalesce(sum({number_selection}),0)'''
            elif self.fields['date_level'][0] == 'Week':
                min_max_sql = f'''select min(date({date_selection}, 'weekday 1', '-7 days')) as min_date_level, max(date({date_selection}, 'weekday 1', '-7 days')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'weekday 1', '-7 days') as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'weekday 1', '-7 days'), {character_selection}'''
                order_sql = f''' order by date({date_selection} , 'weekday 1', '-7 days') desc, coalesce(sum({number_selection}),0)'''
            elif self.fields['date_level'][0] == 'Month':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of month') as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of month'), {character_selection}'''
                order_sql = f''' order by date({date_selection}, 'start of month') desc, coalesce(sum({number_selection}),0)'''
            elif self.fields['date_level'][0] == 'Quarter':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END), {character_selection}'''
                order_sql = f''' order by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END) desc, coalesce(sum({number_selection}),0) '''
            elif self.fields['date_level'][0] == 'Year':
                min_max_sql = f'''select min(date({date_selection}, 'start of year')) as min_date_level, max(date({date_selection}, 'start of year')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of year') as {date_selection}, {character_selection} as {character_selection}, coalesce(sum({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of year'), {character_selection}'''
                order_sql = f''' order by date({date_selection} , 'start of year') desc, coalesce(sum({number_selection}),0)'''
            if where_filters != '':
                where_sql += ' where ' + where_filters
            else:
                where_filters += ''

            sql_statement = select_sql + where_sql + group_sql + order_sql

        elif self.fields['aggregate'][0] == 'Average':
            if self.fields['date_level'][0] == 'Exact Date':
                min_max_sql = f'''select min(date({date_selection})) as min_date_level, max(date({date_selection})) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}) as {date_selection},  {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}),  {character_selection}'''
                order_sql = f''' order by date({date_selection}) desc, avg({number_selection}) '''
            elif self.fields['date_level'][0] == 'Week':
                min_max_sql = f'''select min(date({date_selection}, 'weekday 1', '-7 days')) as min_date_level, max(date({date_selection}, 'weekday 1', '-7 days')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'weekday 1', '-7 days') as {date_selection}, {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'weekday 1', '-7 days'),  {character_selection}'''
                order_sql = f''' order by date({date_selection} , 'weekday 1', '-7 days') desc, avg({number_selection})'''
            elif self.fields['date_level'][0] == 'Month':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of month') as {date_selection}, {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of month'),  {character_selection}'''
                order_sql = f''' order by date({date_selection} , 'start of month') desc, avg({number_selection})'''
            elif self.fields['date_level'][0] == 'Quarter':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END as {date_selection}, {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END), {character_selection}'''
                order_sql = f''' order by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END) desc, coalesce(sum({number_selection}),0)'''
            elif self.fields['date_level'][0] == 'Year':
                min_max_sql = f'''select min(date({date_selection}, 'start of year')) as min_date_level, max(date({date_selection}, 'start of year')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of year') as {date_selection}, {character_selection} as {character_selection}, coalesce(avg({number_selection}),0) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of year'),  {character_selection}'''
                order_sql = f''' order by date({date_selection} , 'start of year') desc, avg({number_selection}) '''
            if where_filters != '':
                where_sql += ' where ' + where_filters
            else:
                where_filters += ''

            sql_statement = select_sql + where_sql + group_sql + order_sql

        elif self.fields['aggregate'][0] == 'Count':
            if self.fields['date_level'][0] == 'Exact Date':
                min_max_sql = f'''select min(date({date_selection})) as min_date_level, max(date({date_selection})) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}) as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}),  {character_selection}'''
                order_sql = f''' order by date({date_selection}) desc, count(*)'''
            elif self.fields['date_level'][0] == 'Week':
                min_max_sql = f'''select min(date({date_selection}, 'weekday 1', '-7 days')) as min_date_level, max(date({date_selection}, 'weekday 1', '-7 days')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'weekday 1', '-7 days') as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'weekday 1', '-7 days'),  {character_selection}'''
                order_sql = f''' order by date({date_selection} , 'weekday 1', '-7 days') desc, count(*)'''
            elif self.fields['date_level'][0] == 'Month':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of month') as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of month'),  {character_selection}'''
                order_sql = f''' order by date({date_selection} , 'start of month') desc, count(*)'''
            elif self.fields['date_level'][0] == 'Quarter':
                min_max_sql = f'''select min(date({date_selection}, 'start of month')) as min_date_level, max(date({date_selection}, 'start of month')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END), {character_selection}'''
                order_sql = f''' order by (CASE 
  WHEN cast(strftime('%m', {date_selection}) as integer) in (1,4,7,10) THEN date({date_selection}, 'start of month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (2,5,8,11) THEN date({date_selection}, 'start of month', '-1 month')
  WHEN cast(strftime('%m', {date_selection}) as integer) in (3,6,9,12) THEN date({date_selection}, 'start of month', '-2 month')
  ELSE 4 END) desc , count(*) '''
            elif self.fields['date_level'][0] == 'Year':
                min_max_sql = f'''select min(date({date_selection}, 'start of year')) as min_date_level, max(date({date_selection}, 'start of year')) as max_date_level from {self.db_name}'''
                df_date_level_min_max = run_query(min_max_sql)
                # these will be used to filter the dataset after df is create when we do continuous dates (basically this will trim the ends)
                min_date_level = df_date_level_min_max['min_date_level'][0]
                max_date_level = df_date_level_min_max['max_date_level'][0]
                select_sql = f'''select date({date_selection}, 'start of year') as {date_selection}, {character_selection} as {character_selection}, count(*) as {number_selection} from {self.db_name}'''
                group_sql = f''' group by date({date_selection}, 'start of year'),  {character_selection}'''
                order_sql = f''' order by date({date_selection} , 'start of year') desc, count(*)'''
            if where_filters != '':
                where_sql += ' where ' + where_filters
            else:
                where_filters += ''

            sql_statement = select_sql + where_sql + group_sql + order_sql
        print(sql_statement)
        df = run_query(sql_statement)
        data.append(df)
        return data
    def tick_degree(self,parameter,rotation):
        dateformater.parse_date(parameter['dataframe'], self.fields['date'][0], 
                                        parameter['date_format'])
        no=0
        for i in parameter['dataframe'][self.fields['date'][0]+ '_formatted'].unique():
            no+=len(i)
        if no>120:
            degree=90 if rotation=='vertical' else 0
        elif no>100:
            degree=45 if rotation=='vertical' else 0
        elif no>65:
            degree=45 if rotation=='vertical' else 0
        elif no>60:
            degree=0 if rotation=='vertical' else 0
        elif no>40:
            degree=0 if rotation=='vetical' else 0
        else:
            degree=0 if rotation=='vertical' else 0
        return degree
    
    def titles(self):
    #0=regular
    #1=averagge color
    #2=average line
    #3=gradient
    #4=median color
    #5=median line
    #6=regression
    #7=percent increase
    #8=runsum
        title_list=[]
        if self.fields['aggregate'][0]=='Sum':
            title = str(self.fields['number'][0]).replace('_',' ') + \
                             ' by ' + str(self.fields['character'][0]).replace('_',' ') + ' and ' + str(self.fields['date_level'][0]).replace('_',' ')
            #parameter['title']= parameter['title'].title()
        elif self.fields['aggregate'][0]=='Average':
            title = 'Average ' + str(self.fields['number'][0]).replace('_',' ') + \
            ' by ' + str(self.fields['character'][0]).replace('_',' ') + ' and ' + str(self.fields['date_level'][0]).replace('_',' ')
            #parameter['title']= parameter['title'].title()
        elif self.fields['aggregate'][0]=='Count':
            title = 'Record count ' + \
            ' by ' + str(self.fields['character'][0]).replace('_',' ') + ' and ' + str(self.fields['date_level'][0]).replace('_',' ')
            #parameter['title']= parameter['title'].title()
        title= title.title()
        title_list.append(title)

        if self.fields['aggregate'][0]=='Sum':
            title = str(self.fields['number'][0]).replace('_',' ') + \
                             ' by ' + str(self.fields['character'][0]).replace('_',' ') + ' runsum'
            #parameter['title']= parameter['title'].title()
        elif self.fields['aggregate'][0]=='Average':
            title = 'Average ' + str(self.fields['number'][0]).replace('_',' ') + \
            ' by ' + str(self.fields['character'][0]).replace('_',' ') + ' runsum'
            #parameter['title']= parameter['title'].title()
        elif self.fields['aggregate'][0]=='Count':
            title = 'Record count ' + \
            ' by ' + str(self.fields['character'][0]).replace('_',' ') + ' runsum'
            #parameter['title']= parameter['title'].title()
        title= title.title()
        title_list.append(title)

        if self.fields['aggregate'][0]=='Sum':
            title = str(self.fields['character'][0]).replace('_',' ') + ' percent of '+str(self.fields['number'][0]).replace('_',' ') 
                             
            #parameter['title']= parameter['title'].title()
        elif self.fields['aggregate'][0]=='Average':
            title = str(self.fields['character'][0]).replace('_',' ') + ' percent of '+str(self.fields['number'][0]).replace('_',' ') 
            #parameter['title']= parameter['title'].title()
        elif self.fields['aggregate'][0]=='Count':
            title = str(self.fields['character'][0]).replace('_',' ') + ' percent of record count'
            #parameter['title']= parameter['title'].title()
        title= title.title()
        title_list.append(title)
        
        
        return title_list
        
    def __customization(self, parameter, customizations=None, 
                        data_label_degree=90, center_x_position=0, y_limit=None, legend=True,
                        legend_placement='center right',tick_degree='horizontal',title='',
                        data_label_frequency=None,percent_label_frequency=None,total_frequency=None):
        color_palette=['#4E79A7','#A0CBE8', '#F28E2B', '#FFBE7D', '#59A14F', '#8CD17D', '#B6992D',
                        '#F1CE63', '#499894', '#86BCB6', '#E15759', '#FF9D9A', '#79706E', '#BAB0AC',
                        '#D37295', '#FABFD2', '#B07AA1', '#D4A6C8', '#9D7660', '#D7B5A6']*5
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        min_d = parameter['dataframe'][number_selection].min()
        max_d = parameter['dataframe'][number_selection].max()
        
        if y_limit is None:
            if min_d < 0:
                y_limit = [min_d - max_d * 0.25, max_d + max_d * 0.25]
            else:
                y_limit = [0, max_d + max_d * 0.25]

        if customizations is not None:
            if 'title' in customizations:
                parameter['title'] = customizations['title']
            else:
                parameter['title']=self.titles()[0]
            if 'y_limit' in customizations.keys():
                parameter['y_limit'] = customizations['y_limit']
            else:
                parameter['y_limit'] = y_limit

            if 'data_label_offset' in customizations.keys():
                parameter['data_label_offset'] = customizations['data_label_offset']
            else:
                parameter['data_label_offset'] = (parameter['dataframe'][number_selection].max()) * 0.01

            if 'data_label_degree' in customizations.keys():
                parameter['data_label_degree'] = int(customizations['data_label_degree']) if tick_degree=='horizontal' else (360-int(customizations['data_label_degree'])%360)
            else:
                parameter['data_label_degree'] = data_label_degree

            if 'bar_width' in customizations.keys():
                parameter['bar_width'] = customizations['bar_width']
            else:
                parameter['bar_width'] = 0.6
            if 'center_x_position' in customizations.keys():
                parameter['center_x_position'] = customizations['center_x_position']
            else:
                parameter['center_x_position'] = center_x_position

            if 'center_y_offset' in customizations.keys():
                parameter['center_y_offset'] = customizations['center_y_offset']
            else:
                parameter['center_y_offset'] = 0

            if 'center_line_color' in customizations.keys():
                parameter['center_line_color'] = customizations['center_line_color']
            else:
                parameter['center_line_color'] = 'k'

            if 'legend' in customizations.keys():
                parameter['legend'] = customizations['legend']
            else:
                parameter['legend'] = legend

            if 'x_label' in customizations.keys():
                parameter['x_label'] = customizations['x_label']
            else:
                parameter['x_label'] = self.fields['date'][0].replace('_',' ')
            if 'y_label' in customizations.keys():
                parameter['y_label'] = customizations['y_label']
            else:
                parameter['y_label'] = self.fields['number'][0].replace('_',' ')
            if 'background' in customizations.keys():
                parameter['background'] = customizations['background']
            else:
                parameter['background'] = 'white'

            if 'data_label_format' in customizations.keys():
                parameter['data_label_format'] = customizations['data_label_format']
            else:
                parameter['data_label_format'] = None

            if 'data_label_frequency' in customizations.keys():
                parameter['data_label_frequency'] = customizations['data_label_frequency']
            else:
                parameter['data_label_frequency'] = data_label_frequency

            if 'data_label_decimal' in customizations.keys():
                parameter['data_label_decimal'] = customizations['data_label_decimal']
            else:
                parameter['data_label_decimal'] = None

            if 'data_label_type' in customizations.keys():
                parameter['data_label_type'] = customizations['data_label_type']
            else:
                parameter['data_label_type'] = 'normal'
            if 'data_label_format_percent' in customizations.keys():
                parameter['data_label_format_percent'] = customizations['data_label_format_percent']
            else:
                parameter['data_label_format_percent'] = None

            if 'data_label_frequency_percent' in customizations.keys():
                parameter['data_label_frequency_percent'] = customizations['data_label_frequency_percent']
            else:
                parameter['data_label_frequency_percent'] = percent_label_frequency

            if 'data_label_decimal_percent' in customizations.keys():
                parameter['data_label_decimal_percent'] = customizations['data_label_decimal_percent']
            else:
                parameter['data_label_decimal_percent'] = None

            if 'data_label_type_percent' in customizations.keys():
                parameter['data_label_type_percent'] = customizations['data_label_type_percent']
            else:
                parameter['data_label_type_percent'] = 'percentage'
            if 'y_on' in customizations.keys():
                parameter['y_on'] = customizations['y_on']
            else:
                parameter['y_on'] = True
            if 'color_palette' in customizations.keys():
                parameter['color_palette'] = customizations['color_palette']
            else:
                parameter['color_palette'] = color_palette
            if 'title_background' in customizations.keys():
                parameter['title_background'] = customizations['title_background']
            else:
                parameter['title_background'] = '#555555'

            if 'title_text_color' in customizations.keys():
                parameter['title_text_color'] = customizations['title_text_color']
            else:
                parameter['title_text_color'] = 'white'
            if 'below_color' in customizations.keys():
                parameter['below_color'] = customizations['below_color']
            else:
                parameter['below_color'] = '#4E79A7'
            if 'above_color' in customizations.keys():
                parameter['above_color'] = customizations['above_color']
            else:
                parameter['above_color'] = '#A0CBE8'
            if 'data_label_format_axis' in customizations.keys():
                parameter['data_label_format_axis'] = customizations['data_label_format_axis']
            else:
                parameter['data_label_format_axis'] = None
            if 'data_label_frequency_axis' in customizations.keys():
                parameter['data_label_frequency_axis'] = customizations['data_label_frequency_axis']
            else:
                parameter['data_label_frequency_axis'] = None
            if 'data_label_decimal_axis' in customizations.keys():
                parameter['data_label_decimal_axis'] = customizations['data_label_decimal_axis']
            else:
                parameter['data_label_decimal_axis'] = None
            if 'data_label_type_axis' in customizations.keys():
                parameter['data_label_type_axis'] = customizations['data_label_type_axis']
            else:
                parameter['data_label_type_axis'] = 'normal'
            if 'data_label_format_total' in customizations.keys():
                parameter['data_label_format_total'] = customizations['data_label_format_total']
            else:
                parameter['data_label_format_total'] = None

            if 'data_label_frequency_total' in customizations.keys():
                parameter['data_label_frequency_total'] = customizations['data_label_frequency_total']
            else:
                parameter['data_label_frequency_total'] = total_frequency

            if 'data_label_decimal_total' in customizations.keys():
                parameter['data_label_decimal_total'] = customizations['data_label_decimal_total']
            else:
                parameter['data_label_decimal_total'] = None

            if 'data_label_type_total' in customizations.keys():
                parameter['data_label_type_total'] = customizations['data_label_type_total']
            else:
                parameter['data_label_type_total'] = 'normal'
            if 'legend_placement' in customizations.keys():
                parameter['legend_placement'] = customizations['legend_placement']
            else:
                parameter['legend_placement'] = legend_placement
            if 'date_format' in customizations.keys():
                parameter['date_format'] = customizations['date_format']
            else:
                if self.fields['date_level'][0] == 'Exact Date':
                    parameter['date_format'] = 'short date'
                elif self.fields['date_level'][0] == 'Week':
                    parameter['date_format'] = 'week'
                elif self.fields['date_level'][0] == 'Month':
                    parameter['date_format'] = 'short month'
                elif self.fields['date_level'][0] == 'Year':
                    parameter['date_format'] = 'year'
                elif self.fields['date_level'][0] == 'Quarter':
                    parameter['date_format'] = 'short quarter'
            if 'x_tick_degree' in customizations.keys():
                parameter['x_tick_degree'] = customizations['x_tick_degree']
                dateformater.parse_date(parameter['dataframe'], self.fields['date'][0], 
                                        parameter['date_format'])
            else:
                parameter['x_tick_degree'] = self.tick_degree(parameter,tick_degree)
            if 'label_font_size' in customizations.keys():
                parameter['label_font_size']=customizations['label_font_size']
            else:
                parameter['label_font_size']=12
            if 'tick_font_size' in customizations.keys():
                parameter['tick_font_size' ] = customizations['tick_font_size']
            else:
                parameter['tick_font_size' ] =12
            if 'data_label_font_size' in customizations.keys():
                parameter['data_label_font_size' ] = customizations['data_label_font_size']
            else:
                parameter['data_label_font_size' ] =12
            if 'data_label_percent_font_size' in customizations.keys():
                parameter['data_label_percent_font_size' ] = customizations['data_label_percent_font_size' ]
            else:
                parameter['data_label_percent_font_size' ] =12
            if 'data_label_total_font_size' in customizations.keys():
                parameter['data_label_total_font_size'] = customizations['data_label_total_font_size']
            else:
                parameter['data_label_total_font_size'] =12
            if 'title_font_size' in customizations.keys():
                parameter['title_font_size']= customizations['title_font_size']
            else:
                parameter['title_font_size']=18
        else:
            parameter['title']=self.titles()[0]
            parameter['y_limit'] = y_limit
            parameter['data_label_offset'] = (parameter['dataframe'][number_selection].max()) * 0.01
            parameter['data_label_degree'] = data_label_degree
            parameter['bar_width'] = 0.6
            parameter['color_palette'] = color_palette
            parameter['center_x_position'] = center_x_position
            parameter['center_y_offset'] = 0
            parameter['center_line_color'] = 'k'
            parameter['legend'] = legend
            parameter['x_label'] = self.fields['date'][0].replace('_',' ')
            parameter['y_label'] = self.fields['number'][0].replace('_',' ')
            parameter['background'] = 'white'
            parameter['data_label_type'] = 'normal'
            parameter['data_label_decimal'] = None
            parameter['data_label_frequency'] = data_label_frequency
            parameter['data_label_format'] = None
            parameter['data_label_type_percent'] = 'percentage'
            parameter['data_label_decimal_percent'] = None
            parameter['data_label_frequency_percent'] = percent_label_frequency
            parameter['data_label_format_percent'] = None
            parameter['y_on'] = True
            parameter['title_background'] = '#555555'
            parameter['title_text_color'] = 'white'
            parameter['below_color'] = '#4E79A7'
            parameter['above_color'] = '#A0CBE8'
            parameter['data_label_type_axis'] = 'normal'
            parameter['data_label_decimal_axis'] = None
            parameter['data_label_frequency_axis'] = None
            parameter['data_label_format_axis'] = None
            parameter['data_label_frequency_total'] = total_frequency
            parameter['data_label_format_total'] = None
            parameter['data_label_type_total'] = 'normal'
            parameter['data_label_decimal_total'] = None
            parameter['legend_placement'] = legend_placement
            if self.fields['date_level'][0] == 'Exact Date':
                parameter['date_format'] = 'short date'
            elif self.fields['date_level'][0] == 'Week':
                parameter['date_format'] = 'week'
            elif self.fields['date_level'][0] == 'Month':
                parameter['date_format'] = 'short month'
            elif self.fields['date_level'][0] == 'Year':
                parameter['date_format'] = 'year'
            elif self.fields['date_level'][0] == 'Quarter':
                parameter['date_format'] = 'short quarter'
            parameter['x_tick_degree'] = self.tick_degree(parameter,tick_degree)
            parameter['label_font_size']=12
            parameter['tick_font_size' ] =12
            parameter['data_label_font_size' ]=12
            parameter['data_label_percent_font_size' ] =12
            parameter['data_label_total_font_size'] =12
            parameter['title_font_size']=18
        dlf = DataLabelFormatter()
        parameter['dataframe']= dlf.data_label_formatter_by_group(df=parameter['dataframe'], col=number_selection,
                                                         format_=parameter['data_label_format'],
                                                         frequency=parameter['data_label_frequency'],
                                                         type_=parameter['data_label_type'],
                                                         decimal=parameter['data_label_decimal'],
                                                         group_by=date_selection)
        
        return parameter

    def data_function_stackbar_1111_descending(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        print('#################### BEFORE ###################')
        print(df)
        print(df[number_selection])
        # dlf = DataLabelFormatter() df = dlf.data_label_formater(df=df, col=number_selection, format_=None,
        # frequency=None, type_=None, decimal=None) print('###############AFTER ##############################')
        # print(df)
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        y_limit = parameter['max_date_mdg'] + parameter['max_date_mdg'] * 0.2
        
        title="Stacked Bar - {} by {} - Colored by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         data_label_degree=0, y_limit=y_limit, legend_placement='best',title=title,tick_degree='vertical')
        parameter['dataframe'] = parameter['dataframe'].fillna(10)
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        

        return parameter

    def stackbar_1111_descending(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        self.fig = Figure((8, 8), dpi=120)
        index = parameters['dataframe'].unstack().index
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        dlf = DataLabelFormatter()
        total = dlf.data_label_formater(df=parameters['date_agg_df'], col='sum_mdg',
                                        format_=parameters['data_label_format_total'],
                                        frequency=parameters['data_label_frequency_total'],
                                        type_=parameters['data_label_type_total'],
                                        decimal=parameters['data_label_decimal_total'])
        # legend
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                self.fig, ax = plt.subplots(1, 2,
                                            sharey=True,
                                            squeeze=True,
                                            gridspec_kw=dict(width_ratios=[0.8, 0.2]),
                                            figsize=(8, 8))
                ax[1].legend(lines, colors.keys(), loc='best', bbox_to_anchor=[1, 0, 0.2, 1])
                # axis self.ax1 to axis
                axis = self.ax1 = ax[0]
                # remove the right ,top and bottom spines
                ax[1].spines['right'].set_visible(False)
                ax[1].spines['top'].set_visible(False)
                ax[1].spines['bottom'].set_visible(False)
                ax[1].spines['left'].set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[1].get_xaxis().set_visible(False)
            else:
                self.ax1 = self.fig.add_subplot()
                axis = self.ax1
                axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.ax1 = self.fig.add_subplot()
            axis = self.ax1
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        for i in index:
            data = parameters['dataframe'].loc[i][number_selection]
            bottom_positive = list(pd.DataFrame(filter(lambda x: x > 0, data)).values.cumsum())
            bottom_negative = list(pd.DataFrame(filter(lambda x: x < 0, data)).values.cumsum())
            neg = 0
            pos = 0
            bottom = []
            bottom_positive.insert(0, 0)
            bottom_negative.insert(0, 0)
            for j in data:
                if j >= 0:
                    bottom.append(bottom_positive[pos])
                    pos += 1
                else:
                    bottom.append(bottom_negative[neg])
                    neg += 1
            bars = axis.bar(x=i, height=data, bottom=bottom)
            for bar, selection, label in zip(bars,
                                             parameters['dataframe'].loc[i][number_selection].index,
                                             parameters['dataframe'].loc[i]['data_label']):
                if abs(bar.get_height() / parameters['max_date_mdg']) > 0.01:
                    axis.text(x=bar.get_x() + bar.get_width() / 2, \
                              y=bar.get_y() + bar.get_height() / 2,
                              s=label,
                              ha='center',
                              va='center',
                              rotation=parameters['data_label_degree'],
                              fontsize=parameters['data_label_font_size' ])
                bar.set_color(colors[selection])
            if bottom_positive[-1] == 0:
                position = total.loc[i]['sum_mdg'] + parameters['data_label_offset']
            else:
                position = bottom_positive[-1] + parameters['data_label_offset']
            axis.text(x=i,
                      y=position,
                      s=total.loc[i]['data_label'],
                      va='bottom',
                      ha='center',
                      rotation=parameters['data_label_degree'],fontsize=parameters['data_label_total_font_size'])
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        # make data labels visible or in the range of the plot.
        if 45 < abs(parameters['data_label_degree']) % 360 < 315:
            axis.set_ylim(axis.get_ylim()[0], parameters['y_limit'])
        # x,y label and x tick
        axis.set_xlabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_ylabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        date = pd.DataFrame(index.array, columns=['date'])
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_xticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ])
        ticks = pd.DataFrame(axis.get_yticks(), columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=parameters['data_label_format_axis'],
                                              frequency=parameters['data_label_frequency_axis'],
                                              type_=parameters['data_label_type_axis'],
                                              decimal=parameters['data_label_decimal_axis'])['data_label']
        axis.set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        # y axis on of
        axis.spines['left'].set_visible(parameters['y_on'])
        axis.get_yaxis().set_visible(parameters['y_on'])
        # background
        axis.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.4625)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        
        return axis, self.fig

    def data_function_stackbar_1111_descending_percentage(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        print('#################### BEFORE ###################')
        print(df)
        print(df[number_selection])
        # dlf = DataLabelFormatter()
        # df = dlf.data_label_formater(df=df, col=number_selection, format_=None, frequency=None, type_=None, decimal=None)
        # print('###############AFTER ##############################')
        # print(df)
        title=self.titles()[2]
        parameter['title']=self.titles()[2]
        parameter = self.__customization(parameter, customizations,
                                         data_label_degree=0, legend_placement='best',title=self.titles()[2],
                                         total_frequency='no labels',tick_degree='vertical')
        parameter['dataframe'] = parameter['dataframe'].fillna(10)
        parameter['title']=self.titles()[2]
        index = df[date_selection].unique()
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        df['percent'] = 0
        for i in index:
            total = sum(df.loc[i][number_selection])
            df.loc[i, 'percent'] = [round(item / total, 4) for item in df.loc[i][number_selection]]
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        print(df)
        return parameter

    def stackbar_1111_descending_percentage(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        # self.fig.set_size_inches(5, 15, forward=True)
        self.fig = Figure((8, 8), dpi=120)
        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setParent(self.scrollAreaWidgetContents)
        # self.canvas.setGeometry(QtCore.QRect(10+x_axis, 100+y_axis, 400, 450))
        index = parameters['dataframe'].unstack().index
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        dlf = DataLabelFormatter()
        total = dlf.data_label_formater(df=parameters['date_agg_df'], col='sum_mdg',
                                        format_=parameters['data_label_format_total'],
                                        frequency=parameters['data_label_frequency_total'],
                                        type_=parameters['data_label_type_total'],
                                        decimal=parameters['data_label_decimal_total'])
        # legend
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                self.fig, ax = plt.subplots(1, 2,
                                            sharey=True,
                                            squeeze=True,
                                            gridspec_kw=dict(width_ratios=[0.8, 0.2]),
                                            figsize=(8, 8))
                ax[1].legend(lines, colors.keys(), loc='best', bbox_to_anchor=[1, 0, 0.2, 1])
                # axis self.ax1 to axis
                axis = self.ax1 = ax[0]
                # remove the right ,top and bottom spines
                ax[1].spines['right'].set_visible(False)
                ax[1].spines['top'].set_visible(False)
                ax[1].spines['bottom'].set_visible(False)
                ax[1].spines['left'].set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[1].get_xaxis().set_visible(False)
            else:
                self.ax1 = self.fig.add_subplot()
                axis = self.ax1
                axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.ax1 = self.fig.add_subplot()
            axis = self.ax1
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        dlf = DataLabelFormatter()
        percent_labels_df = dlf.data_label_formater(df=parameters['dataframe'].copy(), col='percent',
                                                    format_=parameters['data_label_format_percent'],
                                                    frequency=parameters['data_label_frequency_percent'],
                                                    type_=parameters['data_label_type_percent'],
                                                    decimal=parameters['data_label_decimal_percent'])
        for i in index:
            percent_labels = percent_labels_df.loc[i]['data_label']
            data = (parameters['dataframe'].loc[i][number_selection]/ total.loc[i]['sum_mdg']) * 100
            bottom = list(data.values.cumsum())
            bottom.insert(0, 0)
            bars = axis.bar(x=i, height=data, bottom=bottom[0:-1])
            for bar, selection, label in zip(bars,
                                             parameters['dataframe'].loc[i][number_selection].index,
                                             percent_labels):
                if bar.get_height() > 5:
                    axis.text(x=bar.get_x() + bar.get_width() / 2,
                              y=bar.get_y() + bar.get_height() / 2,
                              s=label,
                              ha='center',
                              va='center',
                              rotation=parameters['data_label_degree'],fontsize=parameters['data_label_percent_font_size' ])
                bar.set_color(colors[selection])
            axis.text(x=i,
                      y=102,
                      s=total.loc[i]['data_label'],
                      va='bottom',
                      ha='center',
                      rotation=parameters['data_label_degree'],fontsize=parameters['data_label_total_font_size'])
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        # make data labels visible or in the range of the plot.
        if 45 < abs(parameters['data_label_degree']) % 360 < 315:
            axis.set_ylim(axis.get_ylim()[0], 118)
        # x,y label and x tick
        ticks = pd.DataFrame(axis.get_yticks()/100, columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=None,
                                              frequency=None,
                                              type_='percentage',
                                              decimal=None)['data_label']
        
        axis.set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        axis.set_xlabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_ylabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        date = pd.DataFrame(index.array, columns=['date'])
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_xticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ])
        # y axis on of
        axis.spines['left'].set_visible(parameters['y_on'])
        axis.get_yaxis().set_visible(parameters['y_on'])
        # background
        axis.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.4625)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis, self.fig

    def data_function_stackbar_horizontal_1111_descending(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        print('#################### BEFORE ###################')
        print(df)
        print(df[number_selection])
        # dlf = DataLabelFormatter() df = dlf.data_label_formater(df=df, col=number_selection, format_=None,
        # frequency=None, type_=None, decimal=None) print('###############AFTER ##############################')
        # print(df)
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        y_limit = parameter['max_date_mdg'] + parameter['max_date_mdg'] * 0.2
        title="Stacked Bar Horizontal - {} by {} - Colored by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         data_label_degree=0, y_limit=y_limit, 
                                         legend_placement='best',title=title)
        parameter['dataframe'] = parameter['dataframe'].fillna(10)
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        


        return parameter

    def stackbar_horizontal_1111_descending(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        self.fig = Figure((8, 8), dpi=120)
        index = parameters['dataframe'].unstack().index
        index=index.sort_values(ascending=False)
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        dlf = DataLabelFormatter()
        total = dlf.data_label_formater(df=parameters['date_agg_df'], col='sum_mdg',
                                        format_=parameters['data_label_format_total'],
                                        frequency=parameters['data_label_frequency_total'],
                                        type_=parameters['data_label_type_total'],
                                        decimal=parameters['data_label_decimal_total'])
        # legend
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                self.fig, ax = plt.subplots(1, 2,
                                            sharey=True,
                                            squeeze=True,
                                            gridspec_kw=dict(width_ratios=[0.8, 0.2]),
                                            figsize=(8, 8))
                ax[1].legend(lines, colors.keys(), loc='best', bbox_to_anchor=[1, 0, 0.2, 1])
                # axis self.ax1 to axis
                axis = self.ax1 = ax[0]
                # remove the right ,top and bottom spines
                ax[1].spines['right'].set_visible(False)
                ax[1].spines['top'].set_visible(False)
                ax[1].spines['bottom'].set_visible(False)
                ax[1].spines['left'].set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[1].get_xaxis().set_visible(False)
                # make data labels visible or in the range of the plot.
                if 0 <= abs(parameters['data_label_degree']) % 360 <= 45 or 315 <= abs(parameters['data_label_degree']) % 360 <=360:
                    axis.set_xlim(axis.get_xlim()[0], parameters['y_limit'])
            else:
                self.ax1 = self.fig.add_subplot()
                axis = self.ax1
                axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.ax1 = self.fig.add_subplot()
            axis = self.ax1
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        for i in index:
            data = parameters['dataframe'].loc[i][number_selection]
            left_positive = list(pd.DataFrame(filter(lambda x: x > 0, data)).values.cumsum())
            left_negative = list(pd.DataFrame(filter(lambda x: x < 0, data)).values.cumsum())
            neg = 0
            pos = 0
            left = []
            left_positive.insert(0, 0)
            left_negative.insert(0, 0)
            for j in data:
                if j >= 0:
                    left.append(left_positive[pos])
                    pos += 1
                else:
                    left.append(left_negative[neg])
                    neg += 1
            bars = axis.barh(y=i,width=data, left=left)
            for bar, selection, label in zip(bars,
                                             parameters['dataframe'].loc[i][number_selection].index,
                                             parameters['dataframe'].loc[i]['data_label']):
                if abs(bar.get_width() / parameters['max_date_mdg']) >= 0.15:
                    axis.text(x=bar.get_x() + bar.get_width() / 2, \
                              y=bar.get_y() + bar.get_height() / 2,
                              s=label,
                              ha='center',
                              va='center',
                              rotation=parameters['data_label_degree'],fontsize=parameters['data_label_font_size' ])
                bar.set_color(colors[selection])
            if left_positive[-1] == 0:
                position = total.loc[i]['sum_mdg'] + parameters['data_label_offset']
            else:
                position = left_positive[-1] + parameters['data_label_offset']
            axis.text(y=i,
                      x=position,
                      s=total.loc[i]['data_label'],
                      va='center',
                      ha='left',
                      rotation=parameters['data_label_degree'],fontsize=parameters['data_label_total_font_size'])
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        # x,y label and x tick
        axis.set_ylabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_xlabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        date = pd.DataFrame(index.array, columns=['date'])
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_yticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ],va='center')
        ticks = pd.DataFrame(axis.get_xticks(), columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=parameters['data_label_format_axis'],
                                              frequency=parameters['data_label_frequency_axis'],
                                              type_=parameters['data_label_type_axis'],
                                              decimal=parameters['data_label_decimal_axis'])['data_label']
        axis.set_xticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        # y axis on of
        axis.spines['left'].set_visible(parameters['y_on'])
        axis.get_yaxis().set_visible(parameters['y_on'])
        # background
        axis.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        
        return axis, self.fig

    def data_function_stackbar_1111_horizontal_descending_percentage(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        print('#################### BEFORE ###################')
        print(df)
        print(df[number_selection])
        # dlf = DataLabelFormatter()
        # df = dlf.data_label_formater(df=df, col=number_selection, format_=None, frequency=None, type_=None, decimal=None)
        # print('###############AFTER ##############################')
        # print(df)
        title=self.titles()[2]
        parameter['title']=self.titles()[2]
        parameter = self.__customization(parameter, customizations,
                                         data_label_degree=0,legend_placement='best',title=title,
                                         total_frequency='no labels')
        parameter['dataframe'] = parameter['dataframe'].fillna(10)
        parameter['title']=self.titles()[2]
        index = df[date_selection].unique()
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        df['percent'] = 0
        for i in index:
            total = sum(df.loc[i][number_selection])
            df.loc[i, 'percent'] = [round(item / total, 4) for item in df.loc[i][number_selection]]
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        print(df)
        y_limit = parameter['max_date_mdg'] + parameter['max_date_mdg'] * 0.2
        
        return parameter

    def stackbar_1111_horizontal_descending_percentage(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        # self.fig.set_size_inches(5, 15, forward=True)
        self.fig = Figure((8, 8), dpi=120)
        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setParent(self.scrollAreaWidgetContents)
        # self.canvas.setGeometry(QtCore.QRect(10+x_axis, 100+y_axis, 400, 450))
        index = parameters['dataframe'].unstack().index
        index=index.sort_values(ascending=False)
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        dlf = DataLabelFormatter()
        total = dlf.data_label_formater(df=parameters['date_agg_df'], col='sum_mdg',
                                        format_=parameters['data_label_format_total'],
                                        frequency=parameters['data_label_frequency_total'],
                                        type_=parameters['data_label_type_total'],
                                        decimal=parameters['data_label_decimal_total'])
        # legend
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                self.fig, ax = plt.subplots(1, 2,
                                            sharey=True,
                                            squeeze=True,
                                            gridspec_kw=dict(width_ratios=[0.8, 0.2]),
                                            figsize=(8, 8))
                ax[1].legend(lines, colors.keys(), loc='best', bbox_to_anchor=[1, 0, 0.2, 1])
                # axis self.ax1 to axis
                axis = self.ax1 = ax[0]
                # remove the right ,top and bottom spines
                ax[1].spines['right'].set_visible(False)
                ax[1].spines['top'].set_visible(False)
                ax[1].spines['bottom'].set_visible(False)
                ax[1].spines['left'].set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[1].get_xaxis().set_visible(False)
                # make data labels visible or in the range of the plot.
                if 0 <= abs(parameters['data_label_degree']) % 360 <= 45 or 315 <= abs(parameters['data_label_degree']) % 360 <=360:
                    axis.set_xlim(axis.get_xlim()[0], 118)
            else:
                self.ax1 = self.fig.add_subplot()
                axis = self.ax1
                axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.ax1 = self.fig.add_subplot()
            axis = self.ax1
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        dlf = DataLabelFormatter()
        percent_labels_df = dlf.data_label_formater(df=parameters['dataframe'].copy(), col='percent',
                                                    format_=parameters['data_label_format_percent'],
                                                    frequency=parameters['data_label_frequency_percent'],
                                                    type_=parameters['data_label_type_percent'],
                                                    decimal=parameters['data_label_decimal_percent'])
        for i in index:
            percent_labels = percent_labels_df.loc[i]['data_label']
            data = (parameters['dataframe'].loc[i][number_selection]/ total.loc[i]['sum_mdg']) * 100
            left= list(data.values.cumsum())
            left.insert(0, 0)
            bars = axis.barh(y=i, width=data, left=left[0:-1])
            for bar, selection, label in zip(bars,
                                             parameters['dataframe'].loc[i][number_selection].index,
                                             percent_labels):
                if bar.get_width() > 10:
                    axis.text(x=bar.get_x() + bar.get_width() / 2,
                              y=bar.get_y() + bar.get_height() / 2,
                              s=label,
                              ha='center',
                              va='center',
                              rotation=parameters['data_label_degree'],fontsize=parameters['data_label_percent_font_size' ])
                bar.set_color(colors[selection])
            axis.text(y=i,
                      x=102,
                      s=total.loc[i]['data_label'],
                      va='center',
                      ha='left',
                      rotation=parameters['data_label_degree'],fontsize=parameters['data_label_total_font_size'])
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
            
        # x,y label and x tick
        ticks = pd.DataFrame(axis.get_xticks()/100, columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=None,
                                              frequency=None,
                                              type_='percentage',
                                              decimal=None)['data_label']
        axis.set_xticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        axis.set_ylabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_xlabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        date = pd.DataFrame(index.array, columns=['date'])
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_yticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ],va='center')
        # y axis on of
        axis.spines['left'].set_visible(parameters['y_on'])
        axis.get_yaxis().set_visible(parameters['y_on'])
        # background
        axis.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis, self.fig
    
    def data_function_line_1111(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        title="Line - {} by {} - Colored by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         data_label_degree=0, legend_placement='best',title=title,
                                         data_label_frequency='no labels',tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        print("data function")
        return parameter

    def line_1111(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        index = parameters['dataframe'].unstack().index
        self.fig = Figure((8, 8), dpi=120)
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        # legend
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                self.fig, ax = plt.subplots(1, 2,
                                            sharey=True,
                                            squeeze=True,
                                            gridspec_kw=dict(width_ratios=[0.8, 0.2]),
                                            figsize=(8, 8))
                ax[1].legend(lines, colors.keys(), loc='best', bbox_to_anchor=[1, 0, 0.2, 1])
                # axis self.ax1 to axis
                axis = self.ax1 = ax[0]
                # remove the right ,top and bottom spines
                ax[1].spines['right'].set_visible(False)
                ax[1].spines['top'].set_visible(False)
                ax[1].spines['bottom'].set_visible(False)
                ax[1].spines['left'].set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[1].get_xaxis().set_visible(False)
            else:
                self.ax1 = self.fig.add_subplot()
                axis = self.ax1
                axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.ax1 = self.fig.add_subplot()
            axis = self.ax1
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        # make data labels visible or in the range of the plot.
        df = parameters['dataframe'].unstack()
        for part in column:
            df[number_selection][part].plot(kind='line', ax=axis, marker='o', ms=1, color=colors[part],
                                            legend=None)
            for x, y, label in zip(range(len(parameters['dataframe'].unstack().index)),
                                   df[number_selection][part],
                                   list(df['data_label'][part])):
                if y < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = y - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = y + parameters['data_label_offset']
                axis.text(x=x,
                          y=y,
                          s=label,
                          ha='center',
                          va=va,
                          rotation=rotation,fontsize=parameters['data_label_font_size' ])
        if 45 < abs(parameters['data_label_degree']) % 360 < 315:
            if parameters['y_limit'][0] == 0:
                axis.set_ylim(0, parameters['y_limit'][1])
            else:
                axis.set_ylim(parameters['y_limit'])
        else:
            y_limit = axis.get_ylim()
            if parameters['y_limit'][0] == 0:
                axis.set_ylim([0, y_limit[1] + parameters['data_label_offset']])
            else:
                axis.set_ylim([y_limit[0] - parameters['data_label_offset'],
                               y_limit[1] + parameters['data_label_offset']])
        if parameters['legend'] and not parameters['legend_placement'] == 'outside':
            axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        # x,y label and x ticks
        ticks = pd.DataFrame(axis.get_yticks(), columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=parameters['data_label_format_axis'],
                                              frequency=parameters['data_label_frequency_axis'],
                                              type_=parameters['data_label_type_axis'],
                                              decimal=parameters['data_label_decimal_axis'])['data_label']
        axis.set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        axis.set_xlabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_ylabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        axis.set_xticks(range(len(parameters['dataframe'].unstack().index)))
        date = pd.DataFrame(index.array, columns=['date'])
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_xticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ])
        # background
        axis.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        # y axis on of
        axis.spines['left'].set_visible(parameters['y_on'])
        axis.get_yaxis().set_visible(parameters['y_on'])
        # title
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis, self.fig
    def data_function_line_1111_lobf(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        title="Line - {} by {} - Colored by {} LOBF".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         data_label_degree=0, legend_placement='best',title=title,
                                         data_label_frequency='no labels',tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        print("data function")
        return parameter

    def line_1111_lobf(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        index = parameters['dataframe'].unstack().index
        self.fig = Figure((8, 8), dpi=120)
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        # legend
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                self.fig, ax = plt.subplots(1, 2,
                                            sharey=True,
                                            squeeze=True,
                                            gridspec_kw=dict(width_ratios=[0.8, 0.2]),
                                            figsize=(8, 8))
                ax[1].legend(lines, colors.keys(), loc='best', bbox_to_anchor=[1, 0, 0.2, 1])
                # axis self.ax1 to axis
                axis = self.ax1 = ax[0]
                # remove the right ,top and bottom spines
                ax[1].spines['right'].set_visible(False)
                ax[1].spines['top'].set_visible(False)
                ax[1].spines['bottom'].set_visible(False)
                ax[1].spines['left'].set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[1].get_xaxis().set_visible(False)
            else:
                self.ax1 = self.fig.add_subplot()
                axis = self.ax1
                axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.ax1 = self.fig.add_subplot()
            axis = self.ax1
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        # make data labels visible or in the range of the plot.
        df = parameters['dataframe'].unstack()
        for part in column:
            df[number_selection][part].plot(kind='line', ax=axis, marker='o', ms=1, color=colors[part],
                                            legend=None)
            lm=LinearRegression()
            X=df[number_selection][part].reset_index().index
            lm.fit(X.values.reshape((-1,1)),df[number_selection][part].fillna(0).values.reshape((-1,1)))
            xlim = axis.get_xlim()
            X=list(X)
            X.extend(list(xlim))
            X.sort()
            y=lm.predict(np.array(X).reshape((-1,1)))
            axis.plot(X,y,ls='--',color=colors[part])
            for x, y, label in zip(range(len(parameters['dataframe'].unstack().index)),
                                   df[number_selection][part],
                                   list(df['data_label'][part])):
                if y < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = y - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = y + parameters['data_label_offset']
                axis.text(x=x,
                          y=y,
                          s=label,
                          ha='center',
                          va=va,
                          rotation=rotation,fontsize=parameters['data_label_font_size' ])
        if 45 < abs(parameters['data_label_degree']) % 360 < 315:
            if parameters['y_limit'][0] == 0:
                axis.set_ylim(0, parameters['y_limit'][1])
            else:
                axis.set_ylim(parameters['y_limit'])
        else:
            y_limit = axis.get_ylim()
            if parameters['y_limit'][0] == 0:
                axis.set_ylim([0, y_limit[1] + parameters['data_label_offset']])
            else:
                axis.set_ylim([y_limit[0] - parameters['data_label_offset'],
                               y_limit[1] + parameters['data_label_offset']])
        if parameters['legend'] and not parameters['legend_placement'] == 'outside':
            axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        # x,y label and x ticks
        ticks = pd.DataFrame(axis.get_yticks(), columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=parameters['data_label_format_axis'],
                                              frequency=parameters['data_label_frequency_axis'],
                                              type_=parameters['data_label_type_axis'],
                                              decimal=parameters['data_label_decimal_axis'])['data_label']
        axis.set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        axis.set_xlabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_ylabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        xlim = axis.get_xlim()
        axis.set_xticks(range(len(parameters['dataframe'].unstack().index)))
        axis.set_xlim([X[0],X[-1]])
        date = pd.DataFrame(index.array, columns=['date'])
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_xticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ])
        # background
        axis.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        # y axis on of
        axis.spines['left'].set_visible(parameters['y_on'])
        axis.get_yaxis().set_visible(parameters['y_on'])
        # title
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis, self.fig

    def data_function_area_1111(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        title="Area - {} by {} - Colored by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         data_label_degree=0, legend_placement='best',title=title,
                                         data_label_frequency='no labels',tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        return parameter

    def area_1111(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        index = parameters['dataframe'].unstack().index
        self.fig = Figure((8, 8), dpi=120)
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        # legend
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                self.fig, ax = plt.subplots(1, 2,
                                            sharey=True,
                                            squeeze=True,
                                            gridspec_kw=dict(width_ratios=[0.8, 0.2]),
                                            figsize=(8, 8))
                ax[1].legend(lines, colors.keys(), loc='best', bbox_to_anchor=[1, 0, 0.2, 1])
                # axis self.ax1 to axis
                axis = self.ax1 = ax[0]
                # remove the right ,top and bottom spines
                ax[1].spines['right'].set_visible(False)
                ax[1].spines['top'].set_visible(False)
                ax[1].spines['bottom'].set_visible(False)
                ax[1].spines['left'].set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[1].get_xaxis().set_visible(False)
            else:
                self.ax1 = self.fig.add_subplot()
                axis = self.ax1
                axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.ax1 = self.fig.add_subplot()
            axis = self.ax1
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        # make data labels visible or in the range of the plot.
        df = parameters['dataframe'].unstack()
        column = df[number_selection].columns
        index = df[number_selection].index
        for part in column:
            axis.fill_between(x=index,
                              y1=0,
                              y2=df[number_selection][part],
                              color=colors[part], alpha=0.5)
            for x, y, label in zip(range(len(parameters['dataframe'].unstack().index)),
                                   df[number_selection][part],
                                   list(df['data_label'][part])):
                if y < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = y - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = y + parameters['data_label_offset']
                axis.text(x=x,
                          y=y,
                          s=label,
                          ha='center',
                          va=va,
                          rotation=rotation,fontsize=parameters['data_label_font_size' ])
        if 45 < abs(parameters['data_label_degree']) % 360 < 315:
            if parameters['y_limit'][0] == 0:
                axis.set_ylim(0, parameters['y_limit'][1])
            else:
                axis.set_ylim(parameters['y_limit'])
        else:
            y_limit = axis.get_ylim()
            if parameters['y_limit'][0] == 0:
                axis.set_ylim([0, y_limit[1] + parameters['data_label_offset']])
            else:
                axis.set_ylim([y_limit[0] - parameters['data_label_offset'],
                               y_limit[1] + parameters['data_label_offset']])
        # x,y label and x ticks
        ticks = pd.DataFrame(axis.get_yticks(), columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=parameters['data_label_format_axis'],
                                              frequency=parameters['data_label_frequency_axis'],
                                              type_=parameters['data_label_type_axis'],
                                              decimal=parameters['data_label_decimal_axis'])['data_label']
        axis.set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        axis.set_xlabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_ylabel(parameters['y_label'],fontsize=parameters['label_font_size'])

        # remove lines from area plot
        for line in axis.get_lines():
            line.remove()
        axis.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        # y axis on of
        axis.spines['left'].set_visible(parameters['y_on'])

        date = pd.DataFrame(index.array, columns=['date'])
        axis.set_xticks(range(len(parameters['dataframe'].unstack().index)))
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_xticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ])
        axis.get_yaxis().set_visible(parameters['y_on'])
        # title
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.4625)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis, self.fig

    def data_function_sidebyside_1111_descending(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        title="SBS Bar - {} by {} - Colored by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         legend_placement='best',title=title,tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        return parameter

    def sidebyside_1111_descending(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setParent(self.scrollAreaWidgetContents)
        # self.canvas.setGeometry(QtCore.QRect(10+x_axis, 100+y_axis, 400, 450))
        indexes = parameters['dataframe'].unstack().index
        columns = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(columns, parameters['color_palette']))
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                ratio = [0.75, 0.25]
                self.fig, self.ax1 = plt.subplots(1, 2, figsize=(8, 8),
                                                  sharey=True,
                                                  gridspec_kw=dict(width_ratios=ratio))
                ax = self.ax1
                ax[-1].legend(lines, colors.keys(), loc='best')
                ax[-1].spines['right'].set_visible(False)
                ax[-1].spines['top'].set_visible(False)
                ax[-1].spines['bottom'].set_visible(False)
                ax[-1].spines['left'].set_visible(False)
                ax[-1].get_yaxis().set_visible(False)
                ax[-1].get_xaxis().set_visible(False)
                axis = self.ax1[0]

            else:
                self.fig = Figure((8, 8), dpi=120)
                self.ax1 = self.fig.subplots()
                axis = self.ax1
                self.ax1.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.fig = Figure((8, 8), dpi=120)
            self.ax1 = self.fig.subplots()
            axis = self.ax1
        # self.fig.set_size_inches(5, 15, forward=True)
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        y = 0
        x_tick = []
        for i, index in enumerate(indexes):
            x = [y+(parameters['bar_width'])*j for j in range(len(parameters['dataframe'].loc[index].index))]
            bars = axis.bar(x=x,
                            height=parameters['dataframe'].loc[index][number_selection],
                            width=parameters['bar_width'])
            for bar, selection, label in zip(bars,
                                             parameters['dataframe'].loc[index][number_selection].index,
                                             parameters['dataframe'].loc[index]['data_label']):
                if bar.get_height() < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = bar.get_height() - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = bar.get_height() + parameters['data_label_offset']
                axis.text(x=bar.get_x() + bar.get_width() / 2,
                          y=y,
                          s=label,
                          ha='center',
                          va=va,
                          rotation=rotation,fontsize=parameters['data_label_font_size' ])
                bar.set_color(colors[selection])
            y = bars[-1].get_x()+1.5
            x_tick.append(sum(x)/len(x))
        ticks = pd.DataFrame(axis.get_yticks(), columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=parameters['data_label_format_axis'],
                                              frequency=parameters['data_label_frequency_axis'],
                                              type_=parameters['data_label_type_axis'],
                                              decimal=parameters['data_label_decimal_axis'])['data_label']
        axis.set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        axis.set_ylim(parameters['y_limit'])
        date = pd.DataFrame(indexes.array, columns=['date'])
        axis.set_xticks(x_tick)
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_xticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ])
        # x,y label and x tick
        axis.set_xlabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_ylabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        axis.get_yaxis().set_visible(parameters['y_on'])
        # background
        self.fig.patch.set_facecolor(parameters['background'])
        axis.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis, self.fig

    def data_function_stackedpane_1111(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        title="Bar Pane - {} by {} - Separated by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         legend=False, legend_placement='best', data_label_degree=0,title=title
                                         ,tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        return parameter

    def stackedpane_1111(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        index = parameters['dataframe'].unstack().index
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                ratio = [0.75, 0.25]
                grid = self.fig.add_gridspec(1, 4)
                legend = self.fig.add_subplot(grid[0, 3:])
                legend.legend(lines, colors.keys(), loc='best')
                legend.spines['right'].set_visible(False)
                legend.spines['top'].set_visible(False)
                legend.spines['bottom'].set_visible(False)
                legend.spines['left'].set_visible(False)
                legend.get_yaxis().set_visible(False)
                legend.get_xaxis().set_visible(False)
            else:
                ratio = [1, 0]
                self.fig.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            ratio = [1, 0]
        self.fig, self.ax1 = plt.subplots(len(column), 2, figsize=(8, 8),
                                          sharex='col',
                                          squeeze=True,
                                          gridspec_kw=dict(width_ratios=ratio))
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)

        axis = self.ax1
        for i in axis[:, 1]:
            i.spines['right'].set_visible(False)
            i.spines['top'].set_visible(False)
            i.spines['bottom'].set_visible(False)
            i.spines['left'].set_visible(False)
            i.get_yaxis().set_visible(False)
            i.get_xaxis().set_visible(False)
        for i, (column, ax) in enumerate(zip(column, axis)):
            bars = ax[0].bar(x=parameters['dataframe'].unstack().index,
                             height=parameters['dataframe'].unstack()[number_selection][column], color=colors[column])
            for bar, label, na, in zip(bars, list(parameters['dataframe'].unstack()['data_label'][column]),
                                       parameters['dataframe'].unstack()[number_selection][column].isnull()):
                if na:
                    continue
                if bar.get_height() < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = bar.get_height() - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = bar.get_height() + parameters['data_label_offset']
                ax[0].text(x=bar.get_x() + bar.get_width() / 2,
                           y=y,
                           s=label,
                           ha='center',
                           va=va,
                           rotation=rotation,fontsize=parameters['data_label_font_size' ])
            ax[0].set_ylim(parameters['y_limit'])
            ticks = pd.DataFrame(ax[0].get_yticks(), columns=['ticks'])
            dlf = DataLabelFormatter()
            tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                                  format_=parameters['data_label_format_axis'],
                                                  frequency=parameters['data_label_frequency_axis'],
                                                  type_=parameters['data_label_type_axis'],
                                                  decimal=parameters['data_label_decimal_axis'])['data_label']
            ax[0].set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
            date = pd.DataFrame(index.array, columns=['date'])
            dateformater.parse_date(date, 'date',
                                    parameters['date_format'])

            ax[0].set_xticklabels(date['date' + '_formatted'],
                                  rotation=parameters['x_tick_degree'],
                                  fontsize=parameters['tick_font_size' ])
            # remove the right ,top and bottom spines
            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)
            ax[0].set_facecolor(parameters['background'])
            ax[0].set_ylabel(str(column).replace('_',''),fontsize=parameters['label_font_size'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis[0][0], self.fig

    def data_function_areapane_1111(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        title="Area Pane - {} by {} - Separated by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         legend=False, data_label_degree=0,title=title,data_label_frequency=None,tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        return parameter

    def areapane_1111(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        index = parameters['dataframe'].unstack().index
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                ratio = [0.75, 0.25]
                grid = self.fig.add_gridspec(1, 4)
                legend = self.fig.add_subplot(grid[0, 3:])
                legend.legend(lines, colors.keys(), loc='best')
                legend.spines['right'].set_visible(False)
                legend.spines['top'].set_visible(False)
                legend.spines['bottom'].set_visible(False)
                legend.spines['left'].set_visible(False)
                legend.get_yaxis().set_visible(False)
                legend.get_xaxis().set_visible(False)
            else:
                ratio = [1, 0]
                self.fig.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            ratio = [1, 0]
        self.fig, self.ax1 = plt.subplots(len(column), 2, figsize=(8, 8),
                                          sharex='col',
                                          squeeze=True,
                                          gridspec_kw=dict(width_ratios=ratio))
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)

        axis = self.ax1
        for i in axis[:, 1]:
            i.spines['right'].set_visible(False)
            i.spines['top'].set_visible(False)
            i.spines['bottom'].set_visible(False)
            i.spines['left'].set_visible(False)
            i.get_yaxis().set_visible(False)
            i.get_xaxis().set_visible(False)
        for i, (column, ax) in enumerate(zip(column, axis)):
            ax[0].fill_between(x=index,
                               y1=0,
                               y2=parameters['dataframe'].unstack()[number_selection][column],
                               color=colors[column])
            for x, y, label, na in zip(range(len(parameters['dataframe'].unstack().index)),
                                       parameters['dataframe'].unstack()[number_selection][column],
                                       list(parameters['dataframe'].unstack()['data_label'][column]),
                                       parameters['dataframe'].unstack()[number_selection][column].isnull()):
                if na:
                    continue
                if y < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = y - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = y + parameters['data_label_offset']
                ax[0].text(x=x,
                           y=y,
                           s=label,
                           ha='center',
                           va=va,
                           rotation=rotation,fontsize=parameters['data_label_font_size' ])
            ax[0].set_ylim(parameters['y_limit'])
            ticks = pd.DataFrame(ax[0].get_yticks(), columns=['ticks'])
            dlf = DataLabelFormatter()
            tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                                  format_=parameters['data_label_format_axis'],
                                                  frequency=parameters['data_label_frequency_axis'],
                                                  type_=parameters['data_label_type_axis'],
                                                  decimal=parameters['data_label_decimal_axis'])['data_label']


            ax[0].set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
            date = pd.DataFrame(index.array, columns=['date'])
            dateformater.parse_date(date, 'date',
                                    parameters['date_format'])

            ax[0].set_xticklabels(date['date' + '_formatted'],
                                  rotation=parameters['x_tick_degree'],
                                  fontsize=parameters['tick_font_size' ])
            # remove the right ,top and bottom spines
            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)
            # background
            ax[0].set_facecolor(parameters['background'])
            ax[0].set_ylabel(str(column).replace('_',''),fontsize=parameters['label_font_size'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis[0][0], self.fig

    def data_function_areastack_1111(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        title="Stacked Area  - {} by {} - Colored by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         legend_placement='best', data_label_degree=0,title=title,
                                         data_label_frequency='no labels',tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        return parameter

    def areastack_1111(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        index = parameters['dataframe'].unstack().index
        self.fig = Figure((8, 8), dpi=120)
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        # legend
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                self.fig, ax = plt.subplots(1, 2,
                                            sharey=True,
                                            squeeze=True,
                                            gridspec_kw=dict(width_ratios=[0.8, 0.2]),
                                            figsize=(8, 8))
                ax[1].legend(lines, colors.keys(), loc='best', bbox_to_anchor=[1, 0, 0.2, 1])
                # axis self.ax1 to axis
                axis = self.ax1 = ax[0]
                # remove the right ,top and bottom spines
                ax[1].spines['right'].set_visible(False)
                ax[1].spines['top'].set_visible(False)
                ax[1].spines['bottom'].set_visible(False)
                ax[1].spines['left'].set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[1].get_xaxis().set_visible(False)
            else:
                self.ax1 = self.fig.add_subplot()
                axis = self.ax1
                axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.ax1 = self.fig.add_subplot()
            axis = self.ax1
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        # remove the right and top spines

        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        # make data labels visible or in the range of the plot.
        # axis.set_ylim((0, parameters['y_limit']))
        df = parameters['dataframe'].unstack().fillna(0)
        axis.stackplot(index, df[number_selection].values.transpose(), colors=colors.values())
        dlf = DataLabelFormatter()
        for i in index:
            cum_sums = list(filter(lambda x: x != 0, df[number_selection].loc[i].cumsum().values))
            data = pd.DataFrame(cum_sums, columns=['cumsum'])
            data_labels = dlf.data_label_formater(df=data, col='cumsum',
                                                  format_=parameters['data_label_format'],
                                                  frequency=parameters['data_label_frequency'],
                                                  type_=parameters['data_label_type'],
                                                  decimal=parameters['data_label_decimal'])['data_label']

            for cum_sum, data_label in zip(cum_sums, data_labels):
                if cum_sum < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    cum_sum = cum_sum - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    cum_sum = cum_sum + parameters['data_label_offset']
                axis.text(x=i,
                          y=cum_sum,
                          s=data_label,
                          ha='center',
                          va=va,
                          rotation=rotation,fontsize=parameters['data_label_font_size' ])
        ticks = pd.DataFrame(axis.get_yticks(), columns=['ticks'])

        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=parameters['data_label_format_axis'],
                                              frequency=parameters['data_label_frequency_axis'],
                                              type_=parameters['data_label_type_axis'],
                                              decimal=parameters['data_label_decimal_axis'])['data_label']
        axis.set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        axis.set_xlabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_ylabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        axis.set_xticks(range(len(parameters['dataframe'].unstack().index)))
        date = pd.DataFrame(index.array, columns=['date'])
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_xticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ])
        axis.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        # y axis on of
        axis.spines['left'].set_visible(parameters['y_on'])
        axis.get_yaxis().set_visible(parameters['y_on'])
        # title
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis, self.fig

    def data_function_linerunsum_1111(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        title=self.titles()[1]
        parameter['title']=self.titles()[1]
        parameter = self.__customization(parameter, customizations,
                                         data_label_degree=0, legend_placement='best',title=title,
                                         data_label_frequency='no labels',tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        parameter['title']=self.titles()[1]
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        print('#############cumsum########')
        print('normal')
        print(df)
        print('cumsum')
        df['cumsum'] = df.groupby(character_selection)[number_selection].cumsum()
        print(df)
        parameter['date_agg_df'] = date_agg
        dlf = DataLabelFormatter()
        min_d = parameter['dataframe']['cumsum'].min()
        max_d = parameter['dataframe']['cumsum'].max()
        if min_d < 0:
            y_limit = [min_d - max_d * 0.2, max_d + max_d * 0.2]
        else:
            y_limit = [0, max_d + max_d * 0.2]
        parameter['y_limit'] = y_limit

        parameter['dataframe'] = dlf.data_label_formater(df=parameter['dataframe'], col='cumsum',
                                                         format_=parameter['data_label_format'],
                                                         frequency=parameter['data_label_frequency'],
                                                         type_=parameter['data_label_type'],
                                                         decimal=parameter['data_label_decimal'])
        return parameter

    def linerunsum_1111(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        index = parameters['dataframe'].unstack().index
        self.fig = Figure((8, 8), dpi=120)
        column = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(column, parameters['color_palette']))
        # legend
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                self.fig, ax = plt.subplots(1, 2,
                                            sharey=True,
                                            squeeze=True,
                                            gridspec_kw=dict(width_ratios=[0.8, 0.2]),
                                            figsize=(8, 8))
                ax[1].legend(lines, colors.keys(), loc='best', bbox_to_anchor=[1, 0, 0.2, 1])
                # axis self.ax1 to axis
                axis = self.ax1 = ax[0]
                # remove the right ,top and bottom spines
                ax[1].spines['right'].set_visible(False)
                ax[1].spines['top'].set_visible(False)
                ax[1].spines['bottom'].set_visible(False)
                ax[1].spines['left'].set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[1].get_xaxis().set_visible(False)
            else:
                self.ax1 = self.fig.add_subplot()
                axis = self.ax1
                axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.ax1 = self.fig.add_subplot()
            axis = self.ax1
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        # make data labels visible or in the range of the plot.
        # axis.set_ylim((0, parameters['y_limit']))
        df = parameters['dataframe'].unstack()
        column = df[number_selection].columns
        for part in column:
            df['cumsum'][part].plot(kind='line', ax=axis, marker='o', ms=1, color=colors[part],
                                    legend=False)
            for x, y, label in zip(range(len(parameters['dataframe'].unstack().index)),
                                   df['cumsum'][part],
                                   list(df['data_label'][part])):
                if y < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = y - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = y + parameters['data_label_offset']
                axis.text(x=x,
                          y=y,
                          s=label,
                          ha='center',
                          va=va,
                          rotation=rotation,fontsize=parameters['data_label_font_size' ])
        if 45 < abs(parameters['data_label_degree']) % 360 < 315:
            if parameters['y_limit'][0] == 0:
                axis.set_ylim(0, parameters['y_limit'][1])
            else:
                axis.set_ylim(parameters['y_limit'])
        else:
            y_limit = axis.get_ylim()
            if parameters['y_limit'][0] == 0:
                axis.set_ylim([0, y_limit[1] + parameters['data_label_offset']])
            else:
                axis.set_ylim([y_limit[0] - parameters['data_label_offset'],
                               y_limit[1] + parameters['data_label_offset']])
        if parameters['legend'] and not parameters['legend_placement'] == 'outside':
            axis.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        # x,y label and x ticks
        ticks = pd.DataFrame(axis.get_yticks(), columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                              format_=parameters['data_label_format_axis'],
                                              frequency=parameters['data_label_frequency_axis'],
                                              type_=parameters['data_label_type_axis'],
                                              decimal=parameters['data_label_decimal_axis'])['data_label']
        axis.set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        axis.set_xlabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_ylabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        axis.set_xticks(range(len(parameters['dataframe'].unstack().index)))
        date = pd.DataFrame(index.array, columns=['date'])
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_xticklabels(date['date' + '_formatted'],
                             rotation=parameters['x_tick_degree'],
                             fontsize=parameters['tick_font_size' ])
        axis.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        # y axis on of
        axis.spines['left'].set_visible(parameters['y_on'])
        axis.get_yaxis().set_visible(parameters['y_on'])
        # title
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis, self.fig

    def data_function_sidebyside_1111_horizontal_descending(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        title="SBS Bar Horizontal - {} by {} - Colored by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         legend_placement='best', data_label_degree=0,
                                         title=title)
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg

        return parameter

    def sidebyside_1111_horizontal_descending(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setParent(self.scrollAreaWidgetContents)
        # self.canvas.setGeometry(QtCore.QRect(10+x_axis, 100+y_axis, 400, 450))
        indexes = parameters['dataframe'].unstack().index
        indexes=indexes.sort_values(ascending=False)
        columns = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(columns, parameters['color_palette']))
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                ratio = [0.75, 0.25]
                self.fig, self.ax1 = plt.subplots(1, 2, figsize=(8, 8),
                                                  gridspec_kw=dict(width_ratios=ratio))
                ax = self.ax1
                ax[-1].legend(lines, colors.keys(), loc='best')
                ax[-1].spines['right'].set_visible(False)
                ax[-1].spines['top'].set_visible(False)
                ax[-1].spines['bottom'].set_visible(False)
                ax[-1].spines['left'].set_visible(False)
                ax[-1].get_yaxis().set_visible(False)
                ax[-1].get_xaxis().set_visible(False)
                axis = self.ax1[0]
                # make data labels visible or in the range of the plot.
                if 0 <= abs(parameters['data_label_degree']) % 360 <= 45 or 315 <= abs(parameters['data_label_degree']) % 360 <=360:
                    axis.set_xlim(axis.get_xlim()[0], parameters['y_limit'][1])

            else:
                self.fig = Figure((8, 8), dpi=120)
                self.ax1 = self.fig.subplots()
                axis = self.ax1
                self.ax1.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            self.fig = Figure((8, 8), dpi=120)
            self.ax1 = self.fig.subplots()
            axis = self.ax1
        # self.fig.set_size_inches(5, 15, forward=True)
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        y1 = 0
        y_tick = []
        for i, index in enumerate(indexes):
            y = [y1 + (parameters['bar_width']) * j for j in range(len(parameters['dataframe'].loc[index].index))]
            bars = axis.barh(y=y,
                              width=parameters['dataframe'].loc[index][number_selection],
                              height=parameters['bar_width'])
            for bar, selection, label in zip(bars,
                                             parameters['dataframe'].loc[index][number_selection].index,
                                             parameters['dataframe'].loc[index]['data_label']):
                if bar.get_width() < 0:
                    x = parameters['data_label_offset']
                else:
                    x = bar.get_width() + parameters['data_label_offset']

                axis.text(x=x,
                           y=bar.get_y() + bar.get_height() / 2,
                           s=label,
                           ha='left',
                           va='center',
                           rotation=parameters['data_label_degree'],fontsize=parameters['data_label_font_size' ])
                bar.set_color(colors[selection])
            y1 = bars[-1].get_y() + 1.5
            y_tick.append(sum(y)/len(y))
        axis.set_xlim(parameters['y_limit'])
        # remove the right and top spines
        axis.spines['right'].set_visible(False)
        axis.spines['top'].set_visible(False)
        axis.get_yaxis().set_visible(parameters['y_on'])
        axis.set_facecolor(parameters['background'])
        ticks = pd.DataFrame(axis.get_xticks(), columns=['ticks'])
        dlf = DataLabelFormatter()
        tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                                  format_=parameters['data_label_format_axis'],
                                                  frequency=parameters['data_label_frequency_axis'],
                                                  type_=parameters['data_label_type_axis'],
                                                  decimal=parameters['data_label_decimal_axis'])['data_label']
        axis.set_xticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
        axis.set_xlabel(parameters['x_label'],fontsize=parameters['label_font_size'])
        axis.set_ylabel(parameters['y_label'],fontsize=parameters['label_font_size'])
        self.fig.patch.set_facecolor(parameters['background'])
        date = pd.DataFrame(indexes.array, columns=['date'])
        axis.set_yticks(y_tick)
        dateformater.parse_date(date, 'date',
                                parameters['date_format'])

        axis.set_yticklabels(date['date' + '_formatted'],
                             fontsize=parameters['tick_font_size' ],
                             rotation=parameters['x_tick_degree'],va='center')
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis, self.fig

    def data_function_pane_averages_1111_colored_by_category(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        parameter = self.__customization(parameter, customizations, legend=False,
                                          legend_placement='best', data_label_degree=0,title='Pane')
        parameter['dataframe'] = parameter['dataframe'].fillna(10)
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        average = df[number_selection].mean()
        character_selection_average = df.groupby(character_selection)[number_selection].agg(['mean']).rename(
            columns={'mean': 'average_mdg'})
        median = df[number_selection].median()
        character_select_median = df.groupby(character_selection)[number_selection].agg(['median']).rename(
            columns={'median': 'median_mdg'})
        parameter['character_selection_average'] = character_selection_average

        print(average)
        print(character_selection_average)
        print(median)
        print(character_select_median)
        return parameter

    def pane_averages_1111_colored_by_category(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        index = parameters['dataframe'].unstack().index
        columns = parameters['dataframe'].unstack()[number_selection].columns
        colors = dict(zip(columns, parameters['color_palette']))
        dlf = DataLabelFormatter()
        average = dlf.data_label_formater(df=parameters['character_selection_average'], col='average_mdg',
                                          format_=parameters['data_label_format'],
                                          frequency=parameters['data_label_frequency'],
                                          type_=parameters['data_label_type'], decimal=parameters['data_label_decimal'])
        if parameters['legend']:
            lines = []
            if parameters['legend_placement'] == 'outside':
                ratio = [0.7, 0.3]
                self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                                  sharex='col',
                                                  squeeze=True,
                                                  gridspec_kw=dict(width_ratios=ratio))
                grid = self.fig.add_gridspec(1, 4)
                avg = []
                for ii, column in enumerate(columns):
                    lines.append(Line2D([0], [0], color=colors[column], lw=2))
                    avg.append('Average:' + average['data_label'].iloc[ii])
                legend = self.fig.add_subplot(grid[0, 3:])
                legend.legend(lines, avg, loc='best')
                legend.spines['right'].set_visible(False)
                legend.spines['top'].set_visible(False)
                legend.spines['bottom'].set_visible(False)
                legend.spines['left'].set_visible(False)
                legend.get_yaxis().set_visible(False)
                legend.get_xaxis().set_visible(False)
        else:
            ratio = [1, 0]
            self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                          sharex='col',
                                          squeeze=True,
                                          gridspec_kw=dict(width_ratios=ratio))
        self.fig.subplots_adjust(left=0, right=0.95,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)

        axis = self.ax1
        for i in axis[:, 1]:
            i.spines['right'].set_visible(False)
            i.spines['top'].set_visible(False)
            i.spines['bottom'].set_visible(False)
            i.spines['left'].set_visible(False)
            i.get_yaxis().set_visible(False)
            i.get_xaxis().set_visible(False)
        for i, (column, ax) in enumerate(zip(columns, axis)):
            bars = ax[0].bar(x=parameters['dataframe'].unstack().index,
                             height=parameters['dataframe'].unstack()[number_selection][column], color=colors[column])
            for bar, label, na, in zip(bars, list(parameters['dataframe'].unstack()['data_label'][column]),
                                       parameters['dataframe'].unstack()[number_selection][column].isnull()):
                if na:
                    continue
                if bar.get_height() < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = bar.get_height() - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = bar.get_height() + parameters['data_label_offset']
                ax[0].text(x=bar.get_x() + bar.get_width() / 2,
                           y=y,
                           s=label,
                           ha='center',
                           va=va,
                           rotation=rotation,fontsize=parameters['data_label_font_size' ])
            x = [-bars[0].get_width(), len(bars) - 1 + (bars[0].get_width())]
            ax[0].plot([x[0], x[1]], [parameters['character_selection_average'].loc[column, 'average_mdg'],
                                      parameters['character_selection_average'].loc[column, 'average_mdg']],
                       color=colors[column])
            ax[0].set_xlim(x)
            ax[0].set_ylim(parameters['y_limit'])
            ticks = pd.DataFrame(ax[0].get_yticks(), columns=['ticks'])
            dlf = DataLabelFormatter()
            tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                                  format_=parameters['data_label_format_axis'],
                                                  frequency=parameters['data_label_frequency_axis'],
                                                  type_=parameters['data_label_type_axis'],
                                                  decimal=parameters['data_label_decimal_axis'])['data_label']
            
            ax[0].set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
            date = pd.DataFrame(index.array, columns=['date'])
            dateformater.parse_date(date, 'date',
                                    parameters['date_format'])

            ax[0].set_xticklabels(date['date' + '_formatted'],
                                  rotation=parameters['x_tick_degree'],
                                  fontsize=parameters['tick_font_size' ])
            # remove the right ,top and bottom spines
            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)
            ax[0].set_ylabel(str(column).replace('_',''))
            ax[0].set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis[0][0], self.fig

    def data_function_pane_averages_1111_above_below_average_Color(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        parameter = self.__customization(parameter, customizations,legend=False,
                                         legend_placement='upper right', data_label_degree=0,title='Pane')
        parameter['dataframe'] = parameter['dataframe'].fillna(10)
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        average = df[number_selection].mean()
        character_selection_average = df.groupby(character_selection)[number_selection].agg(['mean']).rename(
            columns={'mean': 'average_mdg'})
        median = df[number_selection].median()
        character_select_median = df.groupby(character_selection)[number_selection].agg(['median']).rename(
            columns={'median': 'median_mdg'})
        parameter['character_selection_average'] = character_selection_average

        print(average)
        print(character_selection_average)
        print(median)
        print(character_select_median)
        return parameter

    def pane_averages_1111_above_below_average_Color(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        index = parameters['dataframe'].unstack().index
        columns = parameters['dataframe'].unstack()[number_selection].columns
        indexes = [len(parameters['dataframe'].loc[x][number_selection].index) for x in index]
        colors = dict(zip(columns, parameters['color_palette']))
        dlf = DataLabelFormatter()
        average = dlf.data_label_formater(df=parameters['character_selection_average'], col='average_mdg',
                                          format_=parameters['data_label_format'],
                                          frequency=parameters['data_label_frequency'],
                                          type_=parameters['data_label_type'], decimal=parameters['data_label_decimal'])
        if parameters['legend']:
            lines = [Line2D([0], [0], color=parameters['above_color'], lw=4),
                     Line2D([0], [0], color=parameters['below_color'], lw=4)]
            if parameters['legend_placement'] == 'outside':
                ratio = [0.7, 0.3]
                self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                                  sharex='col',
                                                  squeeze=True,
                                                  gridspec_kw=dict(width_ratios=ratio))
                grid = self.fig.add_gridspec(1, 4)
                legend = self.fig.add_subplot(grid[0, 3:])
                avg = []
                for ii, column in enumerate(columns):
                    lines.append(Line2D([0], [0], color=colors[column], lw=2))
                    avg.append('Average:' + average['data_label'].iloc[ii])
                text = ['Above Average', 'Below Average'] + avg
                legend.legend(lines, text, loc='best')
                legend.spines['right'].set_visible(False)
                legend.spines['top'].set_visible(False)
                legend.spines['bottom'].set_visible(False)
                legend.spines['left'].set_visible(False)
                legend.get_yaxis().set_visible(False)
                legend.get_xaxis().set_visible(False)
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        axis = self.ax1
        for i in axis[:, 1]:
            i.spines['right'].set_visible(False)
            i.spines['top'].set_visible(False)
            i.spines['bottom'].set_visible(False)
            i.spines['left'].set_visible(False)
            i.get_yaxis().set_visible(False)
            i.get_xaxis().set_visible(False)
        for i, (column, ax) in enumerate(zip(columns, axis)):
            bars = ax[0].bar(x=index,
                             height=parameters['dataframe'].unstack()[number_selection][column],
                             color=colors[column])
            for bar, label, na, in zip(bars, list(parameters['dataframe'].unstack()['data_label'][column]),
                                       parameters['dataframe'].unstack()[number_selection][column].isnull()):
                if na:
                    continue
                bar.set_color(parameters['above_color'])
                # if the height of a bar is below average, color it with dark yellow
                if bar.get_height() < parameters['character_selection_average'].loc[column, 'average_mdg']:
                    bar.set_color(parameters['below_color'])
                if bar.get_height() < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = bar.get_height() - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = bar.get_height() + parameters['data_label_offset']
                ax[0].text(x=bar.get_x() + bar.get_width() / 2,
                           y=y,
                           s=label,
                           ha='center',
                           va=va,
                           rotation=rotation,fontsize=parameters['data_label_font_size' ])
            max_d = parameters['dataframe'].unstack()[number_selection].max().max()
            min_d = parameters['dataframe'].unstack()[number_selection].min().min()
            if min_d > 0:
                min_d = 0
            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)
            ax[0].set_ylim(parameters['y_limit'])
            ticks = pd.DataFrame(ax[0].get_yticks(), columns=['ticks'])
            dlf = DataLabelFormatter()
            tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                                  format_=parameters['data_label_format_axis'],
                                                  frequency=parameters['data_label_frequency_axis'],
                                                  type_=parameters['data_label_type_axis'],
                                                  decimal=parameters['data_label_decimal_axis'])['data_label']
            ax[0].set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
            date = pd.DataFrame(index.array, columns=['date'])
            dateformater.parse_date(date, 'date',
                                    parameters['date_format'])

            ax[0].set_xticklabels(date['date' + '_formatted'],
                                  rotation=parameters['x_tick_degree'],
                                  fontsize=parameters['tick_font_size' ])
            ax[0].set_facecolor(parameters['background'])
            ax[0].set_ylabel(str(column).replace('_',''))
            # draw average line
            x = [-bars[0].get_width(), len(bars) - 1 + (bars[0].get_width())]
            ax[0].plot([x[0], x[1]], [parameters['character_selection_average'].loc[column, 'average_mdg'],
                                      parameters['character_selection_average'].loc[column, 'average_mdg']],
                       color=colors[column])
            ax[0].set_xlim(x)
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis[0][0], self.fig

    def data_function_pane_whole_average_1111_colored_by_category(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        parameter = self.__customization(parameter, customizations,legend=False,
                                         legend_placement='best', data_label_degree=0,title='Pane')
        parameter['dataframe'] = parameter['dataframe'].fillna(10)
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        average = df[number_selection].mean()
        character_selection_average = df.groupby(character_selection)[number_selection].agg(['mean']).rename(
            columns={'mean': 'average_mdg'})
        median = df[number_selection].median()
        character_select_median = df.groupby(character_selection)[number_selection].agg(['median']).rename(
            columns={'median': 'median_mdg'})
        parameter['character_selection_average'] = character_selection_average

        print(average)
        print(character_selection_average)
        print(median)
        print(character_select_median)
        return parameter

    def pane_whole_average_1111_colored_by_category(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        index = parameters['dataframe'].unstack().index
        columns = parameters['dataframe'].unstack()[number_selection].columns
        indexes = [len(parameters['dataframe'].loc[x][number_selection].index) for x in index]
        colors = dict(zip(columns, parameters['color_palette']))
        dlf = DataLabelFormatter()
        average = dlf.data_label_formater(df=parameters['dataframe'].copy(), col='average',
                                          format_=parameters['data_label_format'],
                                          frequency=parameters['data_label_frequency'],
                                          type_=parameters['data_label_type'],
                                          decimal=parameters['data_label_decimal'])['data_label'].iloc[0]
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            text = list(colors.keys())
            text.append("Average:" + average)
            lines.append(Line2D([0], [0], color=parameters['center_line_color'], lw=2))
            if parameters['legend_placement'] == 'outside':
                ratio = [0.75, 0.25]
                self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                                  sharex='col',
                                                  squeeze=True,
                                                  gridspec_kw=dict(width_ratios=ratio))
                grid = self.fig.add_gridspec(1, 4)
                legend = self.fig.add_subplot(grid[0, 3:])
                legend.legend(lines, text, loc='best')
                legend.spines['right'].set_visible(False)
                legend.spines['top'].set_visible(False)
                legend.spines['bottom'].set_visible(False)
                legend.spines['left'].set_visible(False)
                legend.get_yaxis().set_visible(False)
                legend.get_xaxis().set_visible(False)
        else:
            ratio = [1, 0]
            self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                              sharex='col',
                                              squeeze=True,
                                              gridspec_kw=dict(width_ratios=ratio))

        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        axis = self.ax1
        for i in axis[:, 1]:
            i.spines['right'].set_visible(False)
            i.spines['top'].set_visible(False)
            i.spines['bottom'].set_visible(False)
            i.spines['left'].set_visible(False)
            i.get_yaxis().set_visible(False)
            i.get_xaxis().set_visible(False)
        for i, (column, ax) in enumerate(zip(columns, axis)):
            bars = ax[0].bar(x=parameters['dataframe'].unstack().fillna(0).index,
                             height=parameters['dataframe'].unstack().fillna(0)[number_selection][column],
                             color=colors[column])
            for bar, label, na, in zip(bars, list(parameters['dataframe'].unstack()['data_label'][column]),
                                       parameters['dataframe'].unstack()[number_selection][column].isnull()):
                if na:
                    continue
                if bar.get_height() < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = bar.get_height() - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = bar.get_height() + parameters['data_label_offset']
                ax[0].text(x=bar.get_x() + bar.get_width() / 2,
                           y=y,
                           s=label,
                           ha='center',
                           va=va,
                           rotation=rotation,fontsize=parameters['data_label_font_size' ])
            max_d = parameters['dataframe'].unstack().fillna(0)[number_selection].max().max()
            min_d = parameters['dataframe'].unstack().fillna(0)[number_selection].min().min()
            if min_d > 0:
                min_d = 0
            ax[0].set_ylim(parameters['y_limit'])
            ticks = pd.DataFrame(ax[0].get_yticks(), columns=['ticks'])
            dlf = DataLabelFormatter()
            tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                                  format_=parameters['data_label_format_axis'],
                                                  frequency=parameters['data_label_frequency_axis'],
                                                  type_=parameters['data_label_type_axis'],
                                                  decimal=parameters['data_label_decimal_axis'])['data_label']
            ax[0].set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
            ax[0].set_xticks(range(len(index)))
            date = pd.DataFrame(index.array, columns=['date'])
            dateformater.parse_date(date, 'date',
                                    parameters['date_format'])

            ax[0].set_xticklabels(date['date' + '_formatted'],
                                  rotation=parameters['x_tick_degree'],
                                  fontsize=parameters['tick_font_size' ])
            x = [-bars[0].get_width(), len(bars) - 1 + (bars[0].get_width())]
            ax[0].plot([x[0], x[1]], [parameters['average'], parameters['average']],
                       color=parameters['center_line_color'])
            ax[0].set_xlim(x)
            # remove the right ,top and bottom spines
            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)
            ax[0].set_facecolor(parameters['background'])
            ax[0].set_ylabel(str(column).replace('_',''))
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis[0][0], self.fig

    def data_function_pane_whole_average_1111_above_below_average_Color(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        parameter = self.__customization(parameter, customizations,legend=False,
                                         legend_placement='best', data_label_degree=0,title='Pane')
        parameter['dataframe'] = parameter['dataframe'].fillna(10)
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        average = df[number_selection].mean()
        character_selection_average = df.groupby(character_selection)[number_selection].agg(['mean']).rename(
            columns={'mean': 'average_mdg'})
        median = df[number_selection].median()
        character_select_median = df.groupby(character_selection)[number_selection].agg(['median']).rename(
            columns={'median': 'median_mdg'})
        parameter['character_selection_average'] = character_selection_average
        print(parameter['dataframe'])
        print(average)
        print(character_selection_average)
        print(median)
        print(character_select_median)
        return parameter

    def pane_whole_average_1111_above_below_average_Color(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        index = parameters['dataframe'].unstack().index
        columns = parameters['dataframe'].unstack().fillna(0)[number_selection].columns
        indexes = [len(parameters['dataframe'].loc[x][number_selection].index) for x in index]
        colors = dict(zip(columns, parameters['color_palette']))
        dlf = DataLabelFormatter()
        average = dlf.data_label_formater(df=parameters['dataframe'].copy(), col='average',
                                          format_=parameters['data_label_format'],
                                          frequency=parameters['data_label_frequency'],
                                          type_=parameters['data_label_type'],
                                          decimal=parameters['data_label_decimal'])['data_label'].iloc[0]
        if parameters['legend']:
            lines = [Line2D([0], [0], color=parameters['above_color'], lw=4),
                     Line2D([0], [0], color=parameters['below_color'], lw=4),
                     Line2D([0], [0], color=parameters['center_line_color'], lw=2)]

            if parameters['legend_placement'] == 'outside':
                ratio = [0.75, 0.25]
                self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                                  sharex='col',
                                                  squeeze=True,
                                                  gridspec_kw=dict(width_ratios=ratio))
                grid = self.fig.add_gridspec(1, 4)
                legend = self.fig.add_subplot(grid[0, 3:])
                legend.legend(lines, ['Above Average', 'Below Average', "Average:" + average])
                legend.spines['right'].set_visible(False)
                legend.spines['top'].set_visible(False)
                legend.spines['bottom'].set_visible(False)
                legend.spines['left'].set_visible(False)
                legend.get_yaxis().set_visible(False)
                legend.get_xaxis().set_visible(False)

        else:
            ratio = [1, 0]
            self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                              sharex='col',
                                              squeeze=True,
                                              gridspec_kw=dict(width_ratios=ratio))

        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)
        axis = self.ax1
        for i in axis[:, 1]:
            i.spines['right'].set_visible(False)
            i.spines['top'].set_visible(False)
            i.spines['bottom'].set_visible(False)
            i.spines['left'].set_visible(False)
            i.get_yaxis().set_visible(False)
            i.get_xaxis().set_visible(False)
        for i, (column, ax) in enumerate(zip(columns, axis)):
            bars = ax[0].bar(x=parameters['dataframe'].unstack().index,
                             height=parameters['dataframe'].unstack()[number_selection][column], color=colors[column])
            for bar, label, na, in zip(bars, list(parameters['dataframe'].unstack()['data_label'][column]),
                                       parameters['dataframe'].unstack()[number_selection][column].isnull()):
                if na:
                    continue
                bar.set_color(parameters['above_color'])
                # if the height of a bar is below average, color it with dark yellow
                if bar.get_height() < parameters['average']:
                    bar.set_color(parameters['below_color'])
                if bar.get_height() < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = bar.get_height() - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = bar.get_height() + parameters['data_label_offset']
                ax[0].text(x=bar.get_x() + bar.get_width() / 2,
                           y=y,
                           s=label,
                           ha='center',
                           va=va,
                           rotation=rotation,fontsize=parameters['data_label_font_size' ])
            max_d = parameters['dataframe'].unstack()[number_selection].max().max()
            min_d = parameters['dataframe'].unstack()[number_selection].min().min()
            if min_d > 0:
                min_d = 0

            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)
            ax[0].set_ylim(parameters['y_limit'])
            ticks = pd.DataFrame(ax[0].get_yticks(), columns=['ticks'])
            dlf = DataLabelFormatter()
            tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                                  format_=parameters['data_label_format_axis'],
                                                  frequency=parameters['data_label_frequency_axis'],
                                                  type_=parameters['data_label_type_axis'],
                                                  decimal=parameters['data_label_decimal_axis'])['data_label']

            ax[0].set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
            date = pd.DataFrame(index.array, columns=['date'])
            dateformater.parse_date(date, 'date',
                                    parameters['date_format'])

            ax[0].set_xticklabels(date['date' + '_formatted'],
                                  rotation=parameters['x_tick_degree'],
                                  fontsize=parameters['tick_font_size' ])
            x = [-bars[0].get_width(), len(bars) - 1 + (bars[0].get_width())]
            ax[0].plot([x[0], x[1]], [parameters['average'], parameters['average']],
                       color=parameters['center_line_color'])
            ax[0].set_xlim(x)
            ax[0].set_facecolor(parameters['background'])
            ax[0].set_ylabel(str(column).replace('_',''))
        self.fig.patch.set_facecolor(parameters['background'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis[0][0], self.fig

    def data_function_stackedpane_1111_runsum(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        title="Bar Pane - RunSum - {} by {} - Separated by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         legend=False, legend_placement='best', 
                                         data_label_degree=0, title=title,tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['title']=self.titles()[1]
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        print('#############cumsum########')
        print('normal')
        print(df)
        print('cumsum')
        df['cumsum'] = df.groupby(character_selection)[number_selection].cumsum()
        print(df)
        parameter['date_agg_df'] = date_agg
        min_d = parameter['dataframe']['cumsum'].min()
        max_d = parameter['dataframe']['cumsum'].max()
        if min_d < 0:
            y_limit = [min_d - max_d * 0.2, max_d + max_d * 0.2]
        else:
            y_limit = [0, max_d + max_d * 0.2]
        parameter['y_limit'] = y_limit
        dlf = DataLabelFormatter()
        parameter['dataframe'] = dlf.data_label_formater(df=parameter['dataframe'], col='cumsum',
                                                         format_=parameter['data_label_format'],
                                                         frequency=parameter['data_label_frequency'],
                                                         type_=parameter['data_label_type'],
                                                         decimal=parameter['data_label_decimal'])
        return parameter

    def stackedpane_1111_runsum(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        index = parameters['dataframe'].unstack().index
        columns = parameters['dataframe'].unstack()[number_selection].columns
        indexes = [len(parameters['dataframe'].loc[x][number_selection].index) for x in index]
        colors = dict(zip(columns, parameters['color_palette']))
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                ratio = [0.75, 0.25]
                grid = self.fig.add_gridspec(1, 4)
                legend = self.fig.add_subplot(grid[0, 3:])
                legend.legend(lines, colors.keys(), loc='best')
                legend.spines['right'].set_visible(False)
                legend.spines['top'].set_visible(False)
                legend.spines['bottom'].set_visible(False)
                legend.spines['left'].set_visible(False)
                legend.get_yaxis().set_visible(False)
                legend.get_xaxis().set_visible(False)
            else:
                ratio = [1, 0]
                self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                                  sharex='col',
                                                  squeeze=True,
                                                  gridspec_kw=dict(width_ratios=ratio))
                self.fig.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            ratio = [1, 0]
            self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                              sharex='col',
                                              squeeze=True,
                                              gridspec_kw=dict(width_ratios=ratio))
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)

        axis = self.ax1
        for i in axis[:, 1]:
            i.spines['right'].set_visible(False)
            i.spines['top'].set_visible(False)
            i.spines['bottom'].set_visible(False)
            i.spines['left'].set_visible(False)
            i.get_yaxis().set_visible(False)
            i.get_xaxis().set_visible(False)
        for i, (column, ax) in enumerate(zip(columns, axis)):
            bars = ax[0].bar(x=parameters['dataframe'].unstack().index,
                             height=parameters['dataframe'].unstack()['cumsum'][column], color=colors[column])
            for bar, label, na, in zip(bars, list(parameters['dataframe'].unstack()['data_label'][column]),
                                       parameters['dataframe'].unstack()['cumsum'][column].isnull()):
                if na:
                    continue
                if bar.get_height() < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = bar.get_height() - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = bar.get_height() + parameters['data_label_offset']
                ax[0].text(x=bar.get_x() + bar.get_width() / 2,
                           y=y,
                           s=label,
                           ha='center',
                           va=va,
                           rotation=rotation,fontsize=parameters['data_label_font_size' ])
            max_d = parameters['dataframe'].unstack()['cumsum'].max().max()
            min_d = parameters['dataframe'].unstack()['cumsum'].min().min()
            if min_d > 0:
                min_d = 0
            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)
            ax[0].set_ylim(parameters['y_limit'])
            ticks = pd.DataFrame(ax[0].get_yticks(), columns=['ticks'])
            dlf = DataLabelFormatter()
            tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                                  format_=parameters['data_label_format_axis'],
                                                  frequency=parameters['data_label_frequency_axis'],
                                                  type_=parameters['data_label_type_axis'],
                                                  decimal=parameters['data_label_decimal_axis'])['data_label']
            ax[0].set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
            ax[0].set_xticks(range(len(index)))
            date = pd.DataFrame(index.array, columns=['date'])
            dateformater.parse_date(date, 'date',
                                    parameters['date_format'])

            ax[0].set_xticklabels(date['date' + '_formatted'],
                                  rotation=parameters['x_tick_degree'],
                                  fontsize=parameters['tick_font_size' ])
            # remove the right ,top and bottom spines
            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)

            # background
            ax[0].set_facecolor(parameters['background'])
            ax[0].set_ylabel(str(column).replace('_',''),fontsize=parameters['label_font_size'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis[0][0], self.fig

    def data_function_areapane_1111_runsum(self, data, customizations=None):
        parameter = dict()
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        df = data[0].copy()
        average = df[number_selection].mean()
        median = df[number_selection].median()
        parameter['dataframe'] = df
        parameter['average'] = average
        parameter['median'] = median
        df_with_extras = df
        df_with_extras['average'] = average
        df_with_extras['median'] = median
        parameter['df_with_extras'] = df_with_extras
        title="Area Pane - RunSum - {} by {} - Separated by {}".format(number_selection.replace('_',' '),date_selection.replace('_',' '),character_selection.replace('_',' '))
        parameter = self.__customization(parameter, customizations,
                                         legend=False, legend_placement='best', 
                                         data_label_degree=0,title=title,
                                         data_label_frequency='no labels',tick_degree='vertical')
        df = parameter['dataframe'].set_index([date_selection, character_selection])
        parameter['dataframe'] = df
        date_agg = df.groupby(date_selection)[number_selection].agg(['sum', 'max']).rename(
            columns={'sum': 'sum_mdg', 'max': 'max_mdg'})
        max_bar = date_agg['sum_mdg'].max()
        parameter['max_date_mdg'] = max_bar
        date_agg['max_date_mdg'] = max_bar
        parameter['date_agg_df'] = date_agg
        print('#############cumsum########')
        print('normal')
        print(df)
        print('cumsum')
        df['cumsum'] = df.groupby(character_selection)[number_selection].cumsum()
        min_d = parameter['dataframe']['cumsum'].min()
        max_d = parameter['dataframe']['cumsum'].max()
        if min_d < 0:
            y_limit = [min_d - max_d * 0.2, max_d + max_d * 0.2]
        else:
            y_limit = [0, max_d + max_d * 0.2]
        parameter['y_limit'] = y_limit
        print(df)
        parameter['date_agg_df'] = date_agg
        dlf = DataLabelFormatter()
        parameter['dataframe'] = dlf.data_label_formater(df=parameter['dataframe'], col='cumsum',
                                                         format_=parameter['data_label_format'],
                                                         frequency=parameter['data_label_frequency'],
                                                         type_=parameter['data_label_type'],
                                                         decimal=parameter['data_label_decimal'])
        return parameter

    def areapane_1111_runsum(self, parameters, kind, fields):
        number_selection = self.fields['number'][0]
        date_selection = self.fields['date'][0]
        character_selection = self.fields['character'][0]
        index = parameters['dataframe'].unstack().index
        columns = parameters['dataframe'].unstack()[number_selection].columns
        indexes = [len(parameters['dataframe'].loc[x][number_selection].index) for x in index]
        colors = dict(zip(columns, parameters['color_palette']))
        if parameters['legend']:
            lines = []
            for value in colors.values():
                lines.append(Line2D([0], [0], color=value, lw=2))
            if parameters['legend_placement'] == 'outside':
                ratio = [0.75, 0.25]
                self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                                  sharex='col',
                                                  squeeze=True,
                                                  gridspec_kw=dict(width_ratios=ratio))
                grid = self.fig.add_gridspec(1, 4)
                legend = self.fig.add_subplot(grid[0, 3:])
                legend.legend(lines, colors.keys(), loc='best')
                legend.spines['right'].set_visible(False)
                legend.spines['top'].set_visible(False)
                legend.spines['bottom'].set_visible(False)
                legend.spines['left'].set_visible(False)
                legend.get_yaxis().set_visible(False)
                legend.get_xaxis().set_visible(False)
            else:
                ratio = [1, 0]
                self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                                  sharex='col',
                                                  squeeze=True,
                                                  gridspec_kw=dict(width_ratios=ratio))
                self.fig.legend(lines, colors.keys(), loc=parameters['legend_placement'])
        else:
            ratio = [1, 0]
            self.fig, self.ax1 = plt.subplots(len(columns), 2, figsize=(8, 8),
                                              sharex='col',
                                              squeeze=True,
                                              gridspec_kw=dict(width_ratios=ratio))
        self.fig.subplots_adjust(left=0, right=1,
                                 bottom=0.4, top=0.9,
                                 hspace=0.2, wspace=0.01)

        axis = self.ax1
        for i in axis[:, 1]:
            i.spines['right'].set_visible(False)
            i.spines['top'].set_visible(False)
            i.spines['bottom'].set_visible(False)
            i.spines['left'].set_visible(False)
            i.get_yaxis().set_visible(False)
            i.get_xaxis().set_visible(False)
        for i, (column, ax) in enumerate(zip(columns, axis)):
            ax[0].fill_between(x=index,
                               y1=0,
                               y2=parameters['dataframe'].unstack()['cumsum'][column],
                               color=colors[column])
            for x, y, label, na in zip(range(len(parameters['dataframe'].unstack().index)),
                                       parameters['dataframe'].unstack()['cumsum'][column],
                                       list(parameters['dataframe'].unstack()['data_label'][column]),
                                       parameters['dataframe'].unstack()['cumsum'][column].isnull()):
                if na:
                    continue
                if y < 0:
                    rotation = -parameters['data_label_degree']
                    va = 'top'
                    y = y - parameters['data_label_offset']
                else:
                    rotation = parameters['data_label_degree']
                    va = 'bottom'
                    y = y + parameters['data_label_offset']
                ax[0].text(x=x,
                           y=y,
                           s=label,
                           ha='center',
                           va=va,
                           rotation=rotation,fontsize=parameters['data_label_font_size' ])
            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)
            ax[0].set_ylim(parameters['y_limit'])
            ticks = pd.DataFrame(ax[0].get_yticks(), columns=['ticks'])
            dlf = DataLabelFormatter()
            tick_labels = dlf.data_label_formater(df=ticks, col='ticks',
                                                  format_=parameters['data_label_format_axis'],
                                                  frequency=parameters['data_label_frequency_axis'],
                                                  type_=parameters['data_label_type_axis'],
                                                  decimal=parameters['data_label_decimal_axis'])['data_label']

            ax[0].set_yticklabels(tick_labels,fontsize=parameters['tick_font_size' ])
            ax[0].set_xticks(range(len(index)))
            date = pd.DataFrame(index.array, columns=['date'])
            dateformater.parse_date(date, 'date',
                                    parameters['date_format'])

            ax[0].set_xticklabels(date['date' + '_formatted'],
                                  rotation=parameters['x_tick_degree'],
                                  fontsize=parameters['tick_font_size' ])
            # remove the right ,top and bottom spines
            if i < len(axis) - 1:
                ax[0].get_xaxis().set_visible(False)
            # background
            ax[0].set_facecolor(parameters['background'])
            ax[0].set_ylabel(str(column).replace('_',''),fontsize=parameters['label_font_size'])
        self.fig.patch.set_facecolor(parameters['background'])
        title = self.fig.suptitle(parameters['title'],
                                  backgroundcolor=parameters['title_background'],
                                  color=parameters['title_text_color'], weight='normal'
                                  , fontsize=parameters['title_font_size'],x=0.45)
        bb = title.get_bbox_patch()
        bb.set_boxstyle("ext", pad=0.5, width=1200)
        return axis[0][0], self.fig

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
