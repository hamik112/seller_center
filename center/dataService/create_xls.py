# encoding:utf-8



import xlrd
import  datetime
from openpyxl import Workbook




def create_xls(**params):
    header = params.get("header", "")
    datas = params.get("datas", "")
    if not params.get("filename", ""):
        dd = datetime.datetime.now()
        filename = str(dd.strftime('%Y-%m-%d_%H-%M-%S')) + ".xls"
    else:
        filename = params.get("filename", "")
    wb = Workbook()
    ws1 = wb.active
    ws1.title= "template"
    title_list = header
    ws1.append(title_list)
    for lst in datas:
        ws1.append(list(lst))
    # log2.info("create file: %s" %(str(filename)))
    return wb, filename
