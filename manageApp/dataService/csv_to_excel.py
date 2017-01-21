#coding:utf-8
#导入相应模块
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
import xlwt
import codecs

def csv_to_xls(filename):
    #新建excel文件
    try:
        myexcel = xlwt.Workbook(encoding = 'utf-8')
        #新建sheet页
        mysheet = myexcel.add_sheet("sheet1")
        #打开csv文件，事实证明file和open 效果一样的，网上建议用open打开
        csvfile = codecs.open(filename,"rb", "utf-8")
        #读取文件信息
        reader = csv.reader(csvfile)
        l = 0
        #通过循环获取单行信息
        for line in reader:
            r = 0
            #通过双重循环获取单个单元信息
            for i in line:
                #通过双重循环写入excel表格
                mysheet.write(l,r,i)
                r=r+1
            l=l+1
        #最后保存到excel
        excel_filename = str(filename.split(".")[0]) + ".xls"
        print excel_filename
        myexcel.save(excel_filename)
    except Exception, e:
        print str(e)
        myexcel = xlwt.Workbook(encoding = 'utf-8')
        #新建sheet页
        mysheet = myexcel.add_sheet("sheet1")
        #打开csv文件，事实证明file和open 效果一样的，网上建议用open打开
        csvfile = codecs.open(filename,"rb", "gbk")
        #读取文件信息
        reader = csv.reader(csvfile)
        l = 0
        #通过循环获取单行信息
        for line in reader:
            r = 0
            #通过双重循环获取单个单元信息
            for i in line:
                #通过双重循环写入excel表格
                mysheet.write(l,r,i)
                r=r+1
            l=l+1
        #最后保存到excel
        excel_filename = str(filename.split(".")[0]) + ".xls"
        myexcel.save(excel_filename)

    return excel_filename


