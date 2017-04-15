#-*-coding:utf-8-*-
'''
Created on 2016年3月15日

@author: starmerx_008
'''
import datetime
import sys
import time

import random
import redis
import xlrd
import xlwt
import re

import os
from django.conf import  settings

from manageApp.models import FileUploadOther
from manageApp.tasks import deal_file
UPLOAD_PATH = settings.UPLOAD_PATH
reload(sys)
sys.setdefaultencoding('utf-8')

font0 = xlwt.Font()
font0.name = u'宋体'
font0.height = 240

style = xlwt.XFStyle()
style.font = font0

def write_file_other_handle(file_list):
    try:
        for fileobj in file_list:
            fname = fileobj.name
            xuhao = fname.split('.')[0]
            filename = str(time.time()).replace(".", "") + "_" + fname
            file_path = os.path.join(get_path_other(UPLOAD_PATH), filename)
            with open(file_path, "wb+") as f:
                for chunk in fileobj.chunks():
                    f.write(chunk)
            result_filename = filename.split('.')[0] + '_handled.' + filename.split('.')[1]
            result_filepath = os.path.join(get_path_other(UPLOAD_PATH), result_filename)
            db_file_name = result_filename.split('_')[1]+'_'+result_filename.split('_')[2]
            obj = FileUploadOther.objects.create(file_name = db_file_name,file_path=result_filepath,status ='0')
            deal_file.delay(file_path,xuhao,result_filepath,obj,style)
            print datetime.datetime.now()
            # deal_file(file_path, xuhao, result_filepath, obj)
            print datetime.datetime.now()
    except Exception,e:
        raise e

def get_path_other(path):
    now_date = datetime.datetime.now()
    year = now_date.year
    month = now_date.month
    day = now_date.day
    one_path = os.path.join(path, str(year))
    second_path = os.path.join(one_path, str(month))
    third_path = os.path.join(second_path, str(day))
    if not os.path.exists(third_path):
        os.makedirs(third_path)
    return third_path


def tripZero(strs):
    """踢除日的0前缀"""
    first_arr = strs.split(',')
    second_arr = re.split(r'\s+',first_arr[0])
    second_arr[1] = str(int(second_arr[1]))
    first_arr[0] = ' '.join(second_arr)
    return ','.join(first_arr)




def read_excel(file_name):
    """读取excel表格"""

    data = xlrd.open_workbook(file_name)
    sheet = data.sheets()[0]
    old_month = None
    datas = sheet._cell_values
    _value_obj = {'head':datas[:8]}
    _value_item = {}
    item = []
    for data in datas[8:]:
        data_time_str = data[0]
        data_time_arr = re.split(r'\s+', data_time_str)
        if data_time_arr[3].startswith('0'):
            arr_33 = data_time_arr[3].split(':')
            arr_33[0] = u'12'
            arr_33_str = ':'.join(arr_33)
            data_time_arr[3] = arr_33_str
        in_time = datetime.datetime.strptime(' '.join(data_time_arr[0:5]), '%b %d, %Y %I:%M:%S %p')
        current_month = in_time.month
        if not old_month:
            old_month = current_month
        if old_month != current_month:
            _value_item.update({old_month:item})
            item = []
            old_month = current_month
        else:
            item.append(data)
    _value_item.update({current_month: item})
    _value_obj.update({'data':_value_item})
     # = {'sheet_obj':sheet,'name': sheet.name, 'values': sheet._cell_values, 'nrows': len(sheet._cell_values)}
    return _value_obj


def deal_file2(filepath1,code,year,result_filepath,obj2):
    try:
        old_month = None
        r = redis.Redis(host='127.0.0.1', port='6379')
        redis_open_time_arr = r.get('lcc_' + code).split(' ')
        if not redis_open_time_arr:
            print code+"不存在";
            return

        FBA_long_fee_first_time = datetime.datetime(year=int(year),month=2,day=random.randint(20,25),
                                             hour=random.randint(6,12),minute=random.randint(0,59))
        FBA_long_fee_second_time = datetime.datetime(year=int(year), month=8, day=18,
                                                    hour=random.randint(6, 12), minute=random.randint(0, 59))
        data = read_excel(filepath1)
        data_head = data.get('head')
        datas = data.get('data')
        for month in datas:
            open_time_str = "%s %s:%s:%s AM" % (
            redis_open_time_arr[0], random.randint(6, 12), random.randint(0, 59), random.randint(0, 59))
            month_data = datas.get(month)
            open_time_str_arr2 = open_time_str.split('-')
            open_time_str_arr2[0] = str(year)
            open_time_str_arr2[1] = str(month)
            open_time = datetime.datetime.strptime('-'.join(open_time_str_arr2), '%Y-%m-%d %I:%M:%S %p')

            random_day = random.randint(6, 11)
            fba_fee_time = datetime.datetime(year=int(year),month=int(month),day=random_day,
                                             hour=random.randint(6,12),minute=random.randint(0,59),
                                             )
            print fba_fee_time
            flag1 = False
            flag2 = False
            flag3 = False
            insert_obj = []
            for index,da in enumerate(month_data):
                in_time_str = da[0]
                in_time_arr = re.split(r'\s+', in_time_str)
                if in_time_arr[3].startswith('0'):
                    arr_33 = in_time_arr[3].split(':')
                    arr_33[0] = u'12'
                    arr_33_str = ':'.join(arr_33)
                    in_time_arr[3] = arr_33_str
                in_time = datetime.datetime.strptime(' '.join(in_time_arr[0:5]), '%b %d, %Y %I:%M:%S %p')
                PDTorPST = in_time_arr[5]
                if open_time < in_time and not flag1:
                    insert_data1 = [tripZero(open_time.strftime('%b %d, %Y %I:%M:%S %p')) + ' ' + PDTorPST, str(int(da[1])), 'Service Fee',
                                    '', '', 'Subscription Fee', '', '', '', '', '', '', 0, 0, 0,
                                    0, 0, 0, 0, 0, -39.99, -39.99]
                    insert_obj.append({'index': index, 'data': insert_data1,'date':open_time})
                    flag1 = True
                if fba_fee_time < in_time and not flag2:
                    fee = round(random.uniform(50, 400), 2)
                    insert_data2 = [tripZero(fba_fee_time.strftime('%b %d, %Y %I:%M:%S %p')) + ' ' + PDTorPST, str(int(da[1])), 'FBA Inventory Fee', '', '',
                                    'FBA Inventory Storage Fee', '', '', '', '', '', '', 0, 0, 0, 0, 0, 0,
                                    0, 0, '-' + str(fee), '-' + str(fee)]
                    insert_obj.append({'index': index, 'data': insert_data2,'date':fba_fee_time})
                    flag2 = True
                if str(month) == '2':
                    if FBA_long_fee_first_time <in_time and not flag3:
                        FBA_long_fee = round(random.uniform(300, 600), 2)
                        insert_data3 = [tripZero(FBA_long_fee_first_time.strftime('%b %d, %Y %I:%M:%S %p')) + ' ' + PDTorPST,
                                        str(int(da[1])), 'FBA Inventory Fee', '', '',
                                        'FBA Long-Term Storage Fee', '', '', '', '', '', '', 0, 0, 0, 0, 0, 0,
                                        0, 0, '-' + str(FBA_long_fee), '-' + str(FBA_long_fee)]
                        insert_obj.append({'index': index, 'data': insert_data2, 'date': FBA_long_fee_first_time})
                        flag3 = True
                if str(month) == "8":
                    if FBA_long_fee_second_time < in_time and not flag3:
                        FBA_long_fee = round(random.uniform(300, 600), 2)
                        insert_data3 = [tripZero(FBA_long_fee_second_time.strftime('%b %d, %Y %I:%M:%S %p')) + ' ' + PDTorPST,
                                        str(int(da[1])), 'FBA Inventory Fee', '', '',
                                        'FBA Long-Term Storage Fee', '', '', '', '', '', '', 0, 0, 0, 0, 0, 0,
                                        0, 0, '-' + str(FBA_long_fee), '-' + str(FBA_long_fee)]
                        insert_obj.append({'index': index, 'data': insert_data3, 'date': FBA_long_fee_second_time})
                        flag3 = True
                if flag1 and flag2 and flag3:
                    break;
            insert_obj.sort(key=lambda x: x['date'],reverse=True)
            for obj in insert_obj:
                month_data.insert(obj['index'], obj['data'])
            datas[month] = month_data
        file = xlwt.Workbook()
        table = file.add_sheet('info', cell_overwrite_ok=True)
        j = 0
        for head in data_head:
            for t,h in enumerate(head):
                table.write(j, t, h,style)
            j += 1
        for month in datas:
            data_list = datas.get(month)
            for li in data_list:
                for t,h in enumerate(li):
                    table.write(j, t, h,style)
                j += 1
        file.save(result_filepath)
        obj2.status = 1
        obj2.save()
    except Exception,e:
        obj2.status = 0
        obj2.save()
        raise e


def write_file_other_handle2(file_list):
    try:
        for fileobj in file_list:
            fname = fileobj.name
            code_str = fname.split('.')[0]
            code_arr = code_str.split('-')
            code = '-'.join(code_arr[:2])
            year = code_arr[2]
            filename = str(time.time()).replace(".", "") + "_" + fname
            file_path = os.path.join(get_path_other2(UPLOAD_PATH), filename)
            with open(file_path, "wb+") as f:
                for chunk in fileobj.chunks():
                    f.write(chunk)
            result_filename = filename.split('.')[0] + '_handled.' + filename.split('.')[1]
            result_filepath = os.path.join(get_path_other2(UPLOAD_PATH), result_filename)
            db_file_name = result_filename.split('_')[1]+'_'+result_filename.split('_')[2]
            obj = FileUploadOther.objects.create(file_name = db_file_name,file_path=result_filepath,status ='0',type=2)
            deal_file2(file_path, code,year, result_filepath, obj)
    except Exception,e:
        raise e


def get_path_other2(path):
    now_date = datetime.datetime.now()
    year = now_date.year
    month = now_date.month
    day = now_date.day
    one_path = os.path.join(path, str(year))
    second_path = os.path.join(one_path, str(month))
    third_path = os.path.join(second_path, str(day))
    four_path = os.path.join(third_path, str('other2'))
    if not os.path.exists(four_path):
        os.makedirs(four_path)
    return four_path

