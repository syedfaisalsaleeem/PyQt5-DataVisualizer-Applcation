#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 05:51:26 2020

@author: briansizemore
"""
import pandas

import traceback

class DataLabelFormatter:

    def convert_num_to_string(self, num, format_, currency=False, decimal=2):
        if format_ == 'exact':
            if str(num) == 'nan':
                return ''
            num1 = round(num, 2)
            if num1.is_integer():
                num = str(int(num))
            else:
                num = str(num1)
            if currency:
                return '$' + num
            else:
                return num

        elif format_ == 'formatted_normal':
            if str(num) == 'nan':
                return ''
            else:
                num = format(num, ',.{decimal}f'.format(decimal=decimal))
                if currency:
                    return '$' + num
                return num

        elif format_ == 'K':
            if str(num) == 'nan':
                return ''
            else:
                num = num / 1000
                num = format(num, ',.{decimal}f'.format(decimal=decimal))
                if currency:
                    return '$' + num + format_
                return num + format_

        elif format_ == 'M':
            if str(num) == 'nan':
                return ''
            else:
                num = num / 1000000
                num = format(num, ',.{decimal}f'.format(decimal=decimal))
                if currency:
                    return '$' + num + format_
                return num + format_

        elif format_ == 'B':
            if str(num) == 'nan':
                return ''
            else:
                num = num / 1000000000
                num = format(num, ',.{decimal}f'.format(decimal=decimal))
                if currency:
                    return '$' + num + format_
                return num + format_

    def check_the_majority_number(self, num):
        if '.' in num:
            num = num.split('.')[0]
        if len(num) == 1 or len(num) == 2:
            self.tens += 1
        elif len(num) == 3:
            self.hundred += 1
        elif len(num) == 4 or len(num) == 5 or len(num) == 6:
            self.thousand += 1
        elif len(num) == 7 or len(num) == 8 or len(num) == 9:
            self.million += 1
        elif len(num) > 9:
            self.billion += 1

    def return_format(self):
        arr = [self.tens, self.hundred, self.thousand, self.million, self.billion]
        max_ = max(arr)
        print(arr)
        print(max_)
        index = arr.index(max_)
        print(index)
        if index == 0 or index == 1:
            return 'formatted_normal'
        elif index == 2:
            return 'K'
        elif index == 3:
            return 'M'
        elif index == 4:
            return 'B'

    def change_num_to_percentage(self, num, decimal):
        if str(num) == 'nan':
            return ''
        num = round(num, 10)
        num = num * 100
        num = format(num, ',.{decimal}f'.format(decimal=decimal))
        return num + '%'

    def data_label_default(self, df, col):
        self.tens = 0
        self.hundred = 0
        self.thousand = 0
        self.million = 0
        self.billion = 0
        df[col] = df[col].astype(str)
        df[col].apply(self.check_the_majority_number)
        check = self.return_format()
        return check

    def data_label_decimal(self, df, number):
        num = str(df[number].iloc[0])
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

    def data_label_frequency(self, df):
        frequency = len(df)
        min_frequency = 24
        if frequency/min_frequency <= 1:
            return 'all'
        if 1 < frequency/min_frequency <= 2:
            return 'every_other'
        if frequency/min_frequency > 2:
            return 'twenty_four'

    def data_label_formater(self, df, col, type_, format_=None, decimal=None, frequency=None):
        if decimal is None:
            decimal = self.data_label_decimal(df, col)
        else:
            decimal = int(decimal)

        if format_ is None:
            format_ = self.data_label_default(df, col)

        if frequency is None:
            frequency = self.data_label_frequency(df)

        if frequency == 'all':
            df['data_label'] = df[col]

        elif frequency == 'no labels':
            df['data_label'] = None

        elif frequency == 'every_other':
            df['data_label'] = df[col]
            length_df = len(df)
            for i in range(length_df):
                if not i % 2 == 0 and not i == len(df) - 1:
                    df['data_label'][i] = None

        elif frequency == 'twenty_four':
            df['data_label'] = df[col]
            length_df = len(df)
            for i in range(length_df):
                if length_df < 24:
                    df['data_label'] = df[col]
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df['data_label'][i] = None

        elif frequency == 'high_low':
            df['data_label'] = df[col].astype(float)
            max_ = df['data_label'].max()
            min_ = df['data_label'].min()
            for i, j in df.iterrows():
                if not (j['data_label'] == max_ or j['data_label'] == min_):
                    df['data_label'][i] = None

        elif frequency == 'high_low_last':
            df['data_label'] = df[col].astype(float)
            max_ = df['data_label'].max()
            min_ = df['data_label'].min()
            for i, j in df.iterrows():
                if not (j['data_label'] == max_ or j['data_label'] == min_) and not i == len(df) - 1:
                    df['data_label'][i] = None

        elif frequency == 'top3': 
            df['data_label'] = df[col].astype(float)
            top3 = df.nlargest(3, 'data_label')
            for i, j in df.iterrows():
                if not (i == top3.index[0] or i == top3.index[1] or i == top3.index[2]):
                    df['data_label'][i] = None

        print("Length of df:", len(df))
        col1 = 'data_label'
        df[col1] = df[col1].astype(float)
        df[col] = df[col].astype(float)

        if type_ == 'normal':
            df['data_label'] = df[col1].apply(self.convert_num_to_string, format_=format_, decimal=decimal)
        elif type_ == 'percentage':
            df['data_label'] = df[col1].apply(self.change_num_to_percentage, decimal=decimal)
        elif type_ == 'currency':
            df['data_label'] = df[col1].apply(self.convert_num_to_string, format_=format_, currency=True, decimal=decimal)
        
        return df
    

    def data_label_formatter_by_group(self, df, col, type_=None, format_=None, decimal=None, frequency=None, group_by=None):

        group = df.groupby(group_by)
        df_group = []
        apply_col=col
        apply_type=type_
        apply_format=format_
        apply_decimal=decimal
        apply_frequency=frequency
        for key, item in group:
            df_group.append(group.get_group(key))
        for df in df_group:

            print(df)

            self.data_label_formater(df, col=apply_col, type_=apply_type, format_=apply_format, frequency=apply_frequency, decimal=apply_decimal)
        resultant_df = pandas.concat(df_group)
        return resultant_df

# import pandas
# dfme=pandas.read_excel('/Users/briansizemore/Desktop/test_file_1.xlsx')
# print(dfme.columns)
# #data_format_test
# def data_label_format(df, col, type_='normal', format_=None, decimal=None, frequency=None):
#     dlf = DataLabelFormatter()
#     returndf=dlf.data_label_formater(df, col, type_, format_, decimal, frequency)
#     return returndf
    
# #we need commas where appropriate always
# #i dont see the decimal taking any effect on currency or and demonination
# #newdf=data_label(df=dfme, col='number',  format_='hundred', frequency='high_low', type_='currency', decimal=1)
# #newdf=data_label(df=dfme, col='number', type_='currency') strangly the 5th record here is not two decimals
# newdf=data_label_format(df=dfme, col='total',  format_=None, decimal=None, frequency=None)
# print(newdf[['total','data_label']])
