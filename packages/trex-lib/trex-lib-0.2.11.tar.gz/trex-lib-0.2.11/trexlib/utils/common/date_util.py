'''
Created on 19 May 2020

@author: jacklok
'''
 
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def parse_date(date_value, date_separator='/', full_year_date_format='%d/%m/%Y', short_year_date_format='%d/%m/%y'):
    if date_value is not None:
        #logging.info('parse_date: date_value=%s', date_value)
        _d_array = date_value.split(date_separator)
        if len(_d_array)==3:
            if len(_d_array[2])==4:
                _datetime = datetime.strptime(date_value, full_year_date_format)
                return _datetime.date()
            elif len(_d_array[2])==2:
                _datetime = datetime.strptime(date_value, short_year_date_format)
                return _datetime.date()
    return None

def parse_datetime(date_value, parse_format='%d-%m-%Y %H:%M:%S'):
    if date_value:
        return datetime.strptime(date_value, parse_format)
    return None

def get_gmt_datetime_from_gmt(gmt):
    now = datetime.now()
    return now + timedelta(hours=gmt)

def convert_datetime_from_gmt_hours(gmt_hours, datetime_value):
    return datetime_value + timedelta(hours=gmt_hours)


def decrease_date(origin_date, year=0, month=0, day=0, hour=0, minute=0, second=0, millisecond=0):
    if year or month or day or hour or minute or second or millisecond:
        origin_date = origin_date - relativedelta(years=year, months=month, days=day, hours=hour,
                                                  minutes=minute, seconds=second)

        if millisecond:
            origin_date = origin_date - timedelta(milliseconds=millisecond)

        return origin_date
    else:
        return origin_date

def increase_date(origin_date, year=0, month=0, day=0, hour=0, minute=0, second=0, millisecond=0):
    if year or month or day or hour or minute or second:
        

        #logging.info('increase_date b4 increase: origin_date=%s', origin_date)
        origin_date = origin_date + relativedelta(years=year, months=month, days=day, hours=hour,
                                                  minutes=minute, seconds=second)

        if millisecond:
            origin_date = origin_date + timedelta(milliseconds=millisecond)

        #logging.info('increase_date after increased: origin_date=%s', origin_date)

        return origin_date
    else:
        return origin_date
