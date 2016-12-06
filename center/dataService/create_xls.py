# encoding:utf-8


import  re
import  locale
import xlrd
import  datetime
from openpyxl import Workbook, styles

nf = styles.numbers.FORMAT_NUMBER_COMMA_SEPARATED1

list_n_list = ['T', 'U']

def create_xls(**params):
    header = params.get("header", "")
    datas = params.get("datas", "")

    if not params.get("filename", ""):
        dd = datetime.datetime.now()
        filename = str(dd.strftime('%Y-%m-%d_%H-%M-%S')) + ".xlsx"
    else:
        filename = params.get("filename", "")
    wb = Workbook()
    ws1 = wb.active
    ws1.title= "template"
    title_list = header
    ws1.append(title_list)
    n = 1
    for lst in datas:
        tmp_list = []
        for i in lst:
            if lst.index(i)==0:
                tmp_list.append(datetime_to_str(i))
                pass
            else:
                if is_number(i):
                    tmp_list.append(deal_number(i))
                else:
                    tmp_list.append(i)
        ws1.append(list(tmp_list))
        if lst[2].replace(" ","").lower() == "transfer":
            for ni in list_n_list:
                _cell_ni = ws1.cell( ni + str(n + 1))
                _cell_ni.number_format = nf
        n += 1
    return wb, filename


def is_number(strnum):
    """ 判断是否是正常的数字:或者是正常的小数"""
    # regex = re.compile(r"^(-?\d+)(\.\d*)?$")
    regex = re.compile(r"^[-+]{0,1}[0-9]{1,}.{0,1}[0-9]{0,}")
    if re.match(regex, strnum):
        return True
    else:
        return False


def deal_number(mnumber):
    """ 处理下金额数字，处理前面不带0,
        如, 0090 --> 90, 030.03 --> 30.03
    """
    try:
        af_money = int(mnumber)
    except:
        try:
            af_money = float(mnumber)
        except:
            af_money = mnumber
    return af_money



def datetime_to_str(dt):
    return dt.strftime("%b %d, %Y %I:%M:%S %p PDT") #PDT, PST
