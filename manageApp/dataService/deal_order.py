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

import os
from django.conf import  settings

from manageApp.models import FileUploadOther
from manageApp.tasks import deal_file
UPLOAD_PATH = settings.UPLOAD_PATH
reload(sys)
sys.setdefaultencoding('utf-8')
def read_excel(file_name):
    """读取excel表格"""

    data = xlrd.open_workbook(file_name)
    sheets = data.sheets()
    _value_list = [{'name': sheet.name, 'values': sheet._cell_values, 'nrows': len(sheet._cell_values)} for sheet in
                   sheets]
    return _value_list


# def deal_file(filepath,code,result_filepath,obj):
#     try:
#         r = redis.Redis(host='127.0.0.1', port='6379')
#         # data = read_excel('/tmp/source_data.xls' )
#         data = read_excel(filepath)
#         data_head = data[0]['values'][:8]
#         data_head[7].append('internal_sku')
#         data_head[7].append('asin')
#         data_head[7].append('hky')
#         data_head[7].append('xuhao')
#         data_head[7].append('wangguan')
#         data_list = data[0]['values'][8:]
#         i=0
#         for li in data_list:
#             print i
#             """
#             li[0]:date/time
#             li[1]:settlement id
#             li[2]:type
#             li[3]:order id
#             li[4]:sku
#             li[5]:description
#             li[6]:quantity
#             li[7]:marketplace
#             li[7]:fulfillment
#             li[9]:order city
#             li[10]:order state
#             li[11]:order postal
#             li[12]:product sales
#             li[13]:shipping credits
#             li[14]:gift wrap credits
#             li[15]:promotional rebates
#             li[16]:sales tax collected
#             li[17]:selling fees
#             li[18]:fba fees
#             li[17]:other transaction fees
#             li[20]:other
#             li[21]:total
#             """
#             internal_sku = r.hget(li[4], 'sku')
#             asin = r.hget(li[4], 'asin')
#             li.append(internal_sku)
#             li.append(asin)
#             if internal_sku:
#                 if r.hget('asin_' + internal_sku, 'fba'):
#                     li.append('haiyun')
#                 else:
#                     li.append('kongyun')
#             else:
#                 li.append('')
#             if r.get('xh_'+code):
#                 li.append(code)
#                 li.append(r.get('xh_'+code))
#             i=i+1
#         data_count = len(data_list)
#         order_id_list_len = data_count * 3
#         order_id_list = []
#         for order_id in range(order_id_list_len):
#             order_id_list.append(random.randint(1000000, 9999999))
#         order_list = list(set(order_id_list))
#
#         ss = 0
#         address_list = []
#         for li in data_list:
#             if li[3]:
#                 address = [li[9], li[10], li[11]]
#                 address_list.append(address)
#             else:
#                 continue
#         random.shuffle(address_list)
#
#         address_i = 0
#         for li in data_list:
#             """
#             li[0]:date/time
#             li[1]:settlement id
#             li[2]:type
#             li[3]:order id
#             li[4]:sku
#             li[5]:description
#             li[6]:quantity
#             li[7]:marketplace
#             li[7]:fulfillment
#             li[9]:order city
#             li[10]:order state
#             li[11]:order postal
#             li[12]:product sales
#             li[13]:shipping credits
#             li[14]:gift wrap credits
#             li[15]:promotional rebates
#             li[16]:sales tax collected
#             li[17]:selling fees
#             li[18]:fba fees
#             li[19]:other transaction fees
#             li[20]:other
#             li[21]:total
#             li[22]:internal_sku
#             li[23]:asin
#             li[24]:海空运输
#             li[25]:xuhao
#             li[26]:wangguandaima
#             """
#             if li[3]:
#                 if li[2] == 'Chargeback Refund' or li[2] == 'A-to-z Guarantee Claim' or li[2] == 'order' or li[2] == 'refund':
#                     if r.get('addr_' + li[3]):
#                         li[9] = eval(r.get('addr_' + li[3]))[0]
#                         li[10] = eval(r.get('addr_' + li[3]))[1]
#                         li[11] = eval(r.get('addr_' + li[3]))[2]
#                     else:
#                         r.set('addr_' + li[3], str(address_list[address_i]))
#                         li[9] = address_list[address_i][0]
#                         li[10] = address_list[address_i][1]
#                         li[11] = address_list[address_i][2]
#                 if r.get('orderid_'+li[3]):
#                     li[3] = r.get('orderid_'+li[3])
#                 else:
#                     old_li3 = li[3]
#                     li[3] = li[3][:4] + str(order_list[ss]) + '-'
#                     ss += 1
#                     li[3] += str(order_list[ss])
#                     ss += 1
#                     r.set('orderid_'+old_li3, li[3])
#                 li[12] = (round(li[12] * 1.01, 2))
#                 li[21] = (
#                 float(li[12]) + float(li[13]) + float(li[14]) + float(li[15]) + float(li[16]) + float(li[17]) + float(
#                     li[18]) + float(li[19]) + float(li[20]))
#                 if li[22]:
#                     li[4] = r.hget('asin_' + li[23], 'newoutsku')
#                 if len(li) == 25:
#                     print li[24]
#                 address_i += 1
#             else:
#                 continue
#
#         j = 0
#         file = xlwt.Workbook()
#         table = file.add_sheet('info', cell_overwrite_ok=True)
#         for head in data_head:
#             t = 0
#             for h in head:
#                 table.write(j, t, head[t])
#                 t += 1
#             j += 1
#
#         for li in data_list:
#             t = 0
#             for h in li:
#                 table.write(j, t, li[t])
#                 t += 1
#             j += 1
#
#         j = 0
#         file.save(result_filepath)
#         obj.status = 1
#         obj.save()
#     except Exception,e:
#         obj.status = 2
#         obj.save()
#         raise e

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
            deal_file.delay(file_path,xuhao,result_filepath,obj)
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
