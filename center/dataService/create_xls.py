# encoding:utf-8


import  re
import  locale
import xlrd
import  datetime
from openpyxl import Workbook, styles




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
    for lst in datas:
        tmp_list = []
        for i in lst:
            if is_number(i):
                if lst.index(i) >11:
                    tmp_list.append(format_str(i))
                else:
                    tmp_list.append(deal_number(i))
            else:
                tmp_list.append(i)
        ws1.append(list(tmp_list))
        # _cell = ws1.cell('T1')
        # nf = styles.numbers.FORMAT_NUMBER_COMMA_SEPARATED1
        # _cell.style.number_format = nf
        # log2.info("create file: %s" %(str(filename)))
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


def format_str(num):
    num = deal_number(num)
    if num >= 1000 or num <= -1000:
        try:
            return number_format(num,2)
        except Exception:
            return num
    else:
        return num


def number_format(num, places=0):

    """Format a number according to locality and given places"""

    locale.setlocale(locale.LC_ALL, "")

    return locale.format("%.*f", (places, num), True)