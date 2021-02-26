from PyQt5 import QtCore, QtGui, QtWidgets
from sqlalchemy import create_engine,event,Column ,Integer,String,ForeignKey
import pandas as pd
from matplotlib.path import Path
from matplotlib.patches import BoxStyle
import re
from dateutil.parser import parse
import time
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
import sys
from os.path import expanduser
from sys import platform
import requests
import json
import pickle
import base64




def resource_path():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return base_path

BASE_DIR = resource_path()
print(BASE_DIR)
#renamed database
home = ''
if platform == 'darwin':
    home = expanduser('~')
    engine = create_engine(f'''sqlite:///{home}/vizpick.db''', echo=True,)
else:
    engine = create_engine(f'''sqlite:///.//vizpick.db''', echo=True,)

api_key = "b'948bcd379eee73da1ab80"

web_url = 'https://api.vizpick.com'

class LoadThread(QtCore.QThread):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)

    # run method gets called when we start the thread
    def run(self):
        time.sleep(1)
        self.signal.emit()

class MySplashScreen(QtWidgets.QSplashScreen):

    def mousePressEvent(self, event):
    # disable default "click-to-dismiss" behaviour
        pass

def delete_datasource(name):
    '''
        This function deletes the datasource of the given object
    '''
    print(name,"name")
    connection = engine.connect()
    connection.execute(f"DROP TABLE IF EXISTS {name}")
    connection.execute(f"DELETE from meta_data where dbname= '{name}' ")
    connection.close()

def logout_user_from_db():
    Session = sessionmaker(bind=engine)
    session = Session()
    session.execute(f"delete from user_info;")
    session.commit()
    session.close()

def show_error_message(text_):
    ''' 
        This function creates a dialogue box for error
    '''
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(text_)
    msg.setWindowTitle("VizPick")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    msg.exec_()


def show_success_message(text_):
    '''
        This function creates a dialogue box for successs
    '''
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text_)
    msg.setWindowTitle("VizPick")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()

def run_query(sql_query):
    """
        This function is used to bring data from the database using the query
    """
    df = pd.read_sql_query(sql_query, engine)
    return df

class ExtendedTextBox(BoxStyle._Base):
    """
    An Extended Text Box that expands to the axes limits 
                        if set in the middle of the axes
    """

    def __init__(self, pad=0.3, width=500.):
        """
        width: 
            width of the textbox. 
            Use `ax.get_window_extent().width` 
                   to get the width of the axes.
        pad: 
            amount of padding (in vertical direction only)
        """
        self.width=width
        self.pad = pad
        super(ExtendedTextBox, self).__init__()

    def transmute(self, x0, y0, width, height, mutation_size):
        """
        x0 and y0 are the lower left corner of original text box
        They are set automatically by matplotlib
        """
        # padding
        pad = mutation_size * self.pad

        # we add the padding only to the box height
        height = height + 2.*pad
        # boundary of the padded box
        y0 = y0 - pad
        y1 = y0 + height
        _x0 = x0
        x0 = _x0 +width /2. - self.width/2.
        x1 = _x0 +width /2. + self.width/2.

        cp = [(x0, y0),
              (x1, y0), (x1, y1), (x0, y1),
              (x0, y0)]

        com = [Path.MOVETO,
               Path.LINETO, Path.LINETO, Path.LINETO,
               Path.CLOSEPOLY]

        path = Path(cp, com)

        return path

def guess_data_types(df):
    mydict=dict()
    for column in df.columns:
        mydict[column]={}
    for column in df.columns:
        if df[column].dtypes in ('int64', 'float64'):
            mydict[column]['datatype']='NUMBER'
        elif  1==1:
            try:
                parse(df[column][20])
                mydict[column]['datatype']='DATE'
            except:
                mydict[column]['datatype']='CHARACTER'
    return mydict

def clean_headers(dataframe):
    try:
        headers=dataframe.columns
        new_headers=[]
        for item in headers:
            new_header=re.sub('[^A-Za-z0-9]+', '_', item)
            new_headers.append(new_header)
        dataframe.columns=new_headers
        return dataframe
    except Exception as e:
        print(e)
        return dataframe

def lookup(date_pd_series, format=None):
    dates = {date:pd.to_datetime(date, dayfirst=False) for date in date_pd_series.unique()}
    return date_pd_series.map(dates)

def enforce_data_types(df, metadata):
    for key in metadata.keys():
        try:
            if metadata[key]['datatype']=='NUMBER':
                df[key]=pd.to_numeric(df[key], errors='coerce')
                df[key] = df[key].astype(float)
                #df['DataFrame Column'] = df['DataFrame Column'].fillna(0)
            elif metadata[key]['datatype']=='DATE':
                df[key] = lookup(df[key])
            else:
                df[key]= df[key].astype(str)
        except Exception as e:
            #show_error_message("Sorry, we can't convert "+ str(key) + " to " + metadata[key]['datatype'] )
            print('#cantconvert')
            print(e)
            metadata[key]['datatype']='CHARACTER'
            df[key]= df[key].astype(str)

    return df

def convert_num_to_string(num,format_,currency=False,decimal=2):
    num = float(num)
    #num = float('{:.3g}'.format(num))
    if format_ == 'ten':
        num = "%0.*f" % (decimal, num)
        if currency:
            return '$' + num 
        return num 

    elif format_ == 'hundred':
        num = "%0.*f" % (decimal, num)
        if currency:
            return '$' + num 
        return num 
    
    elif format_ == 'K':
        num = "%0.*f" % (decimal, num/1000)
        print(num)
        if currency:
            return '$' + num + format_
        return num + format_

    elif format_ == 'M':
        num = "%0.*f" % (decimal, num / 1000000)
        if currency:
            return '$' + num + format_
        return num + format_
         
    elif format_ == 'B':
        num = "%0.*f" % (decimal, num / 100000000)
        if currency:
            return '$' + num + format_
        return num + format_
    elif format_ == 'T':
        num = "%0.*f" % (decimal, num / 1000000000000)
        if currency:
            return '$' + num + format_
        return num + format_


tens = 0
hundred = 0     
thousand = 0
million = 0
billion = 0

def check_the_majority_number(num):
    #num = float(num)
    global tens
    global hundred
    global thousand
    global million
    global billion
    if '.' in num:
        num = num.split('.')[0]
    if len(num) == 2:
        tens += 1
    elif len(num) == 3:
        hundred += 1
    elif len(num) == 4:
        thousand += 1
    elif len(num) == 7:
        million += 1
    elif len(num) != 9:
        billion += 1
    
def return_format():
    arr = [tens,hundred,thousand,million,billion]
    max_ = max(arr)
    print(arr)
    print(max_)
    index = arr.index(max_)
    print(index)
    if index == 0:
        return 'ten'
    elif index == 1:
        return 'hundred'
    elif index == 2:
        return 'K'
    elif index == 3:
        return 'M'
    elif index == 4:
        return 'B'




def change_num_to_currency(num):
    num = float(num)
    return"${:,.2f}".format(num)

def change_num_to_percentage(num,decimal):
    num = float(num)
    num = "%0.*f" % (decimal, num * 100)
    num += '%'
    return num

def data_label_default(df,col):
    df[col] = df[col].astype(str)
    check = df[col].apply(check_the_majority_number)
    check = return_format()
    return check

def data_label_decimal(df, number):
    num = str(df[number][0])
    count = 0
    if '.' in num:
        check_n = num.split('.')[1]
        for i in check_n:
            if i == '0':
                count += 1
    if count == num[::-1].find('.'):
        return 0
    n_decimal = num[::-1].find('.')
    if int(n_decimal) > 2:
        return 2
    elif n_decimal == -1:
        return 0
    return n_decimal

def data_label_format(df,col,type_='Standard',format_=None,decimal=None,actual=None):
    if decimal == None:
        decimal = data_label_decimal(df,col)
    if format_ == None:
        format_ = data_label_default(df,col)
    if type_ == 'Standard':
        df['data_label'] = df[col].apply(convert_num_to_string,format_=format_,decimal=decimal)
    elif type_ == 'percent':
        df['data_label'] = df[col].apply(change_num_to_percentage,decimal=decimal)
    elif type_ == 'currency':
        if actual:
            df['data_label'] = df[col].apply(change_num_to_currency)
        else:

            df['data_label'] = df[col].apply(convert_num_to_string,format_=format_,currency=True)
    elif type_ == 'percent':
        df['data_label'] = df[col].apply(change_num_to_percentage)
    df[col] = df[col].astype(float)
    return df



def where_function(self):
    where_character=''
    if not bool(self.selection_characters):
        where_character=''
    else:
        for key in self.selection_characters.keys():
            # if selection_character[key]!=range_character[key]:
            if where_character=='':
                where_character=str(key)+ ' in (' + str(self.selection_characters[key]).replace('[','').replace(']','') + ')'
            else:
                where_character+= ' and ' + str(key)+ ' in (' + str(self.selection_characters[key]).replace('[','').replace(']','') + ')'
    where_number=''
    for key in self.selection_numbers.keys():
            if int(self.selection_numbers[key][0]) != int(float(self.range_number[key][0])) or int(self.selection_numbers[key][1]) != int(float(self.range_number[key][1])):
                if where_number=='':
                    where_number=str(key)+ ' between ' + str(int(self.selection_numbers[key][0])) + ' and '+ str(int(self.selection_numbers[key][1])) + ''
                else:
                    where_number+= ' and ' +str(key)+ ' between ' + str(int(self.selection_numbers[key][0])) + ' and '+ str(int(self.selection_numbers[key][1])) + ''
    where_date=''
    for key in self.selection_dates.keys():
        print(self.selection_dates[key])
        print(self.range_date[key])
        if self.selection_dates[key] != self.range_date[key]:       
            print('condition true') 
            if where_date=='':
                where_date='date('+str(key)+ ') between ' + "'" +self.selection_dates[key][0]+ "'" + ' and ' + "'" + self.selection_dates[key][1]+ "'" + ''
            else:
                where_date+= ' and date('+ str(key)+ ') between ' + "'" +self.selection_dates[key][0]+ "'" + ' and '+"'" + self.selection_dates[key][1] + "'"+ ''

    where_filters=''
    where_filters+=where_character
    if where_number != "":
        if where_filters=='':
            where_filters+=where_number
        else:
            where_filters+=' and '+ where_number
    if where_date != '':
        if where_filters=='':
            where_filters+=where_date
        else:
            where_filters+=' and '+ where_date
    return where_filters

def hit_api(df):
    pickled = pickle.dumps(df)
    pickled_b64 = base64.b64encode(pickled)
    hug_pickled_str = pickled_b64.decode('utf-8')
    data = {'payload_data':hug_pickled_str}
    headers={'Content-Type': 'application/json' ,'Www-Authorization':str(api_key)}
    r = requests.post(web_url+'/vizpick/data-collect/', data=json.dumps(data), headers=headers)
    print(r.status_code)
    if r.status_code == 200:
        f = open("data.log", "w")
        date = df.iloc[[-1]]['datetime'].values[0]
        f.write(date)
        f.close()

def beta_register_api(df):
    pickled = pickle.dumps(df)
    pickled_b64 = base64.b64encode(pickled)
    hug_pickled_str = pickled_b64.decode('utf-8')
    data = {'payload_data':hug_pickled_str}
    headers={'Content-Type': 'application/json' ,'Www-Authorization':str(api_key)}
    r = requests.post(web_url+'/vizpick/user-signup/', data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        print('successful registration######################')
    else:
        print('notsuccessufl registration#############')
    
    
def send_data_to_api():
        if os.path.isfile('data.log'):
            f = open("data.log", "r")
            date = f.read()
            f.close()
            print(date)
            sql_query = f'''
                select * from data_collection where datetime > '{date}'
            '''
            df = run_query(sql_query)
            print(df)
            if not df.empty:
                hit_api(df)
        else:
            sql_query = f'''
                select * from data_collection
            '''
            df = run_query(sql_query)
            if not df.empty:
                hit_api(df)
    


class DataCollectionThread(QtCore.QThread):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        try:
            print('###########RUNNING#########################')
            send_data_to_api()
        except Exception as e:
            print(e)

def collect_data(type,detail,parent=None):
    try:
        sql_query = f'''
                select * from user_info
        '''
        data = run_query(sql_query)
        user = data['email'][0]
        hash_ = abs(hash(str(time.time())+user))
        data = pd.DataFrame({'user':user,'type':type,'detail':detail,'datetime':datetime.now(),'hash':str(hash_)},index=[0])
        data.to_sql('data_collection',engine,if_exists='append',index=False)
        if parent != None:
            print(parent)
            parent.thread = DataCollectionThread()
            parent.thread.start()
    except Exception as e:
        print('ERROR ON SENDING DATA TO API')
        print(e)


class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()


    def mousePressEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mousePressEvent(self, event)


