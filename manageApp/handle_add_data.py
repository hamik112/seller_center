#-*-coding:utf-8-*-

import datetime
import random
import math
import os
import re
import redis
import xlrd
import xlwt


def tripZero(strs):
    """踢除日的0前缀"""
    first_arr = strs.split(',')
    second_arr = re.split(r'\s+', first_arr[0])
    second_arr[1] = str(int(second_arr[1]))
    first_arr[0] = ' '.join(second_arr)

    second_arr_2 = re.split(r'\s+', first_arr[1])
    third_arr = re.split(r':', second_arr_2[2])
    third_arr[0] = str(int(third_arr[0]))
    second_arr_2[2] = ':'.join(third_arr)
    first_arr[1] = ' '.join(second_arr_2)

    return ','.join(first_arr)

def reversed_cmp(x, y):
    data_time1 = datetime.datetime.strptime(x, '%Y-%m')
    data_time2 = datetime.datetime.strptime(y, '%Y-%m')
    if data_time1 > data_time2:
        return 1
    if data_time1 < data_time2:
        return -1
    return 0

##生成时间得总体集合。
def create_time_set(first_time,end_time = datetime.datetime(2017,5,31,23,59,59)):
    if not first_time:
        return None
    obj = {}
    obj_month = {}
    time_arr = []
    old_year  = first_time.year
    old_month  = first_time.month
    add_arr = [80,83,86]
    next_time =first_time + datetime.timedelta(seconds=add_arr[random.randint(0,2)])
    while next_time<end_time:
        next_time_year = next_time.year
        next_time_month = next_time.month
        if next_time_month != old_month:
            obj_month.update({old_month:time_arr})
            time_arr = []
            time_arr.append(next_time)
            old_month = next_time_month
            if next_time_year != old_year:
                obj.update({old_year:obj_month})
                obj_month = {}
                old_year = next_time_year
        else:
            time_arr.append(next_time)
        next_time = next_time + datetime.timedelta(seconds=add_arr[random.randint(0, 2)])
    obj_month.update({next_time_month:time_arr})
    obj.update({next_time_year: obj_month})
    return obj

##随机生成规定数量的数字
def random_my_num(number,max_num):
    num = 0
    indexs = []
    while num<number:
        indexs.append(random.randint(0,max_num-1))
        num +=1
    indexs.sort()
    return indexs

def write_to_excel(data_head,datas,result_filepath):
    font0 = xlwt.Font()
    font0.name = u'宋体'
    font0.height = 240
    style = xlwt.XFStyle()
    style.font = font0
    file = xlwt.Workbook()
    table = file.add_sheet('Sheet1', cell_overwrite_ok=True)
    j = 0
    for head in data_head:
        for t, h in enumerate(head):
            table.write(j, t, h, style)
        j += 1
    for li in datas:
        for t, h in enumerate(li):
            table.write(j, t, h, style)
        j += 1
    file.save(result_filepath)

def read_excel(file_name):
    """读取excel表格"""

    data = xlrd.open_workbook(file_name)
    sheet = data.sheets()[0]
    return sheet._cell_values

def hanled(filepath1,code,result_filepath):
    try:
        r = redis.Redis(host='127.0.0.1', port='6379')
        redis_open_time = r.hget('lcc_' + code, 'lcc_kdtime')
        redis_first_order_time = r.hget('lcc_' + code, 'lcc_first_order_time')
        proportion = r.hget('lcc_' + code, 'lcc_proportion')
        if not redis_open_time:
            print code + "不存在";
            raise Exception('店铺信息不存在!')
        redis_open_time_arr = redis_open_time.split(' ')
        create_set = create_time_set(datetime.datetime.strptime(redis_first_order_time, '%Y-%m-%d %H:%M:%S'))

        open_time_str = "%s %s:%s:%s AM" % (
        redis_open_time_arr[0], random.randint(6, 12), random.randint(0, 59), random.randint(0, 59))
        open_time_str_arr2 = open_time_str.split('-')
        data = read_excel(filepath1)
        data_head = data[:8]
        datas = data[8:]
        use_time = {}
        insert_obj = []
        j = 0
        PDTorPST = 'PDT'
        settlement_id = datas[0][1]
        old_order_id = None
        proportion_obj = eval(proportion)
        for y_m in proportion_obj:
            if not y_m:
                break
            y_year = y_m.split('-')[0]
            y_month = y_m.split('-')[1]
            number = math.ceil(int(float(proportion_obj.get(y_m)) / 100 * len(datas)))
            base_time = create_set.get(int(y_year)).get(int(y_month))
            my_group_number = random_my_num(int(number), len(base_time))
            use_time.update({y_m: [base_time[index_0] for index_0 in my_group_number]})
        keys = sorted(use_time.keys(), reversed_cmp)
        for key in keys:
            flag1 = True
            flag2 = True
            flag3 = True
            month_use_time = use_time.get(key)
            year = key.split('-')[0]
            month = key.split('-')[1]
            for index, item_time in enumerate(month_use_time):
                new_order_id = datas[j][3]
                open_time_str_arr2[0] = str(year)
                open_time_str_arr2[1] = str(month)
                open_time = datetime.datetime.strptime('-'.join(open_time_str_arr2), '%Y-%m-%d %I:%M:%S %p')
                if j > len(datas) - 1:
                    break
                if old_order_id != new_order_id:
                    datas[j][0] = tripZero(item_time.strftime('%b %d, %Y %I:%M:%S %p')) + ' ' + PDTorPST
                else:
                    if j <= 0:
                        datas[j][0] = datas[j][0]
                    else:
                        datas[j][0] = datas[j - 1][0]
                # 添加service Fee
                if open_time < item_time and flag1:
                    insert_data1 = [tripZero(open_time.strftime('%b %d, %Y %I:%M:%S %p')) + ' ' + PDTorPST,
                                    int(settlement_id),
                                    'Service Fee',
                                    '', '', 'Subscription Fee', '', '', '', '', '', '', 0, 0, 0,
                                    0, 0, 0, 0, 0, -39.99, -39.99]
                    insert_obj.append({'index': j, 'data': insert_data1, 'date': open_time})
                    flag1 = False

                # 添加FBA Inventory Fee
                random_day = random.randint(6, 11)
                fba_fee_time = datetime.datetime(year=int(year), month=int(month), day=random_day,
                                                 hour=random.randint(6, 12), minute=random.randint(0, 59), )
                if fba_fee_time < item_time and flag2:
                    fee = round(random.uniform(-400, -50), 2)
                    insert_data2 = [tripZero(fba_fee_time.strftime('%b %d, %Y %I:%M:%S %p')) + ' ' + PDTorPST,
                                    int(settlement_id),
                                    'FBA Inventory Fee', '', '',
                                    'FBA Inventory Storage Fee', '', '', '', '', '', '', 0, 0, 0, 0, 0, 0,
                                    0, 0, fee, fee]
                    insert_obj.append({'index': j, 'data': insert_data2, 'date': fba_fee_time})
                    flag2 = False

                ##添加二月份的长期仓储费
                if str(month) == '2':
                    FBA_long_fee_first_time = datetime.datetime(year=int(year), month=2,
                                                                day=random.randint(20, 25),
                                                                hour=random.randint(6, 12),
                                                                minute=random.randint(0, 59))
                    if FBA_long_fee_first_time < item_time and flag3:
                        FBA_long_fee = round(random.uniform(-600, -300), 2)
                        insert_data3 = [
                            tripZero(FBA_long_fee_first_time.strftime('%b %d, %Y %I:%M:%S %p')) + ' ' + PDTorPST,
                            int(settlement_id), 'FBA Inventory Fee', '', '',
                            'FBA Long-Term Storage Fee', '', '', '', '', '', '', 0, 0, 0, 0, 0, 0,
                            0, 0, FBA_long_fee, FBA_long_fee]
                        insert_obj.append({'index': j, 'data': insert_data3, 'date': FBA_long_fee_first_time})
                        flag3 = False

                ##添加八月份的长期仓储费
                if str(month) == '8':
                    FBA_long_fee_second_time = datetime.datetime(year=int(year), month=8, day=18,
                                                                 hour=random.randint(6, 12),
                                                                 minute=random.randint(0, 59))
                    if FBA_long_fee_second_time < item_time and flag3:
                        FBA_long_fee = round(random.uniform(300, 600), 2)
                        insert_data3 = [
                            tripZero(FBA_long_fee_second_time.strftime('%b %d, %Y %I:%M:%S %p')) + ' ' + PDTorPST,
                            int(settlement_id), 'FBA Inventory Fee', '', '',
                            'FBA Long-Term Storage Fee', '', '', '', '', '', '', 0, 0, 0, 0, 0, 0,
                            0, 0, FBA_long_fee, FBA_long_fee]
                        insert_obj.append({'index': j, 'data': insert_data3, 'date': FBA_long_fee_second_time})
                        flag3 = False
                old_order_id = new_order_id
                j += 1
        insert_obj.sort(key=lambda x: x['date'], reverse=True)
        for obj in insert_obj:
            datas.insert(obj['index'], obj['data'])

        write_to_excel(data_head, datas, result_filepath)
    except Exception,e:
        raise e


if __name__ == "__main__":
    filepath = '/home/cc/amazon文件处理/test/'
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        if os.path.isfile(child):
            code_str = allDir.split('.')[0]
            code_arr = code_str.split('-')
            code= '-'.join(code_arr[:2])
            result = os.path.join('%s%s%s%s' % (filepath, 'hanled/', code, '_handled.xls'))
            if not os.path.exists(os.path.join('%s%s' % (filepath, 'hanled/'))):
                os.makedirs(os.path.join('%s%s' % (filepath, 'hanled/')))
            print allDir
            print child  # .decode('gbk')是解决中文显示乱码问题
            print result
            try:
                hanled(child, code,result)
                print code + '.xls' + ':\t success!\n\n'
            except Exception, e:
                print str(e)
                print code + '.xls' + ':\t failed!\n\n' + str(e)


