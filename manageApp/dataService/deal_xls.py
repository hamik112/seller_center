# encoding:utf-8

import  os
import logging
import xlrd
import  datetime
from openpyxl import Workbook
import  time

log2 = logging.getLogger("scripts")

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
    print datas
    for lst in datas:
        ws1.append(list(lst))
    log2.info("create file: %s" %(str(filename)))
    return wb, filename



def read_xls(filename):
    time.sleep(1)
    _value_list = []
    if not os.path.exists(filename):
        return {"statue": -1, "msg":"not found file...", "data":_value_list}
    try:
        data = xlrd.open_workbook(filename)
    except Exception, e:
        errors = "open excel Error, %s" % e
        log2.error(errors)
        return {"statue": -2 , "msg": errors, "data":_value_list}
    sheets = data.sheets()
    _value_list = [{'name': sheet.name, 'values': sheet._cell_values, 'nrows': len(sheet._cell_values)} for sheet in
                   sheets]
    return {"statue": 1, "msg":"", "data":_value_list}





def inventory_read_txt(filename):
    _value_list = []
    if not os.path.exists(filename):
        return {"status": -1, "msg":"not found file ...", "data":_value_list}
    try:
        data = open(filename,"r")
    except Exception, e:
        errors = "open %s error" %str(filename)
        log2.error(errors)
        return {'status': -2, "msg":"", "data": _value_list}
    for line in data:
        line = line.replace("\r\n", "")
        _value_list.append(line.split("\t"))
    try:
        data.close()
    except:
        pass
    return {"status": 1, "msg": "", "data": _value_list}