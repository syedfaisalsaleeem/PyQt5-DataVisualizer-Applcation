#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 05:39:39 2021

@author: briansizemore
"""

import pandas as pd
import datetime
import math
def get_quarter(d):
    return "Q%d - %d" % (math.ceil(d.month / 3), d.year)

def parse_date(df, field, c_type):
    parsed_date = []

    if c_type == 'short date':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(datetime.date.strftime(d, "%m/%d/%y"))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'month day':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(datetime.date.strftime(d, "%b %d"))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'long date':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(datetime.date.strftime(d, "%A,%b %d, %Y"))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'month':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(datetime.date.strftime(d, "%B - %Y"))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'year':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(datetime.date.strftime(d, "%Y"))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'date':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(datetime.date.strftime(d, "%Y-%m-%d "))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'short month':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(datetime.date.strftime(d, "%b %Y"))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'median date':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(datetime.date.strftime(d, "%b %d, %Y"))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'quarter':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(get_quarter(d))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'short quarter':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            Q = str(math.ceil(d.month / 3.))
            parsed_date.append(datetime.date.strftime(d, "Q"+Q+"-%y"))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

    elif c_type == 'week':
        for i in df[field]:
            d = datetime.datetime.strptime(i, '%Y-%m-%d')
            parsed_date.append(datetime.date.strftime(d, "Week " + "%V"))
        df[field + '_formatted'] = parsed_date
        for i in range(len(df)):
                if len(df) < 24:
                    df[field + '_formatted'] = df[field + '_formatted']
                elif not i % round(len(df) / 24) == 0 and not i == 0 and not i == len(df) - 1:
                    df[field + '_formatted'][i] = ''

