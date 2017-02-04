# encoding:utf-8
import  time
import  os
from django.conf import  settings
from django.db.models import Q
from manageApp.models import  UploadFileRecorde, StatementView, InventoryUploadRecorde
from manageApp.dataService.dataImport import  StatementViewImport, InventoryReportImport
from manageApp.dataService.tasks_util import update_file_statue
from center.models import InventoryReportsData
from manageApp.dataService.csv_to_excel import csv_to_xls
import  logging

log = logging.getLogger("scripts")

UPLOAD_PATH = settings.UPLOAD_PATH



class FileUpload(object):
    def __init__(self, fileobj_list, username=None):
        self.fileobj_list = fileobj_list
        self.username = username

    def __call__(self, *args, **kwargs):
        return self.write_file()

    def write_file(self, file_upload=None):
        file_list = []
        for fileobj in self.fileobj_list:
            fname = fileobj.name.replace(" ", "")
            if self.username:
                # filename = str(self.username) +"__"+ str(time.time()).replace(".","")+"__" + fname
                filename = fname
            else:
                filename = str(time.time()).replace(".","")+"_" + fname
            file_path = os.path.join(get_path(UPLOAD_PATH), filename)
            with open(file_path, "wb+") as f:
                for chunk in fileobj.chunks():
                    f.write(chunk)
            if file_path.endswith(".csv"):
                file_path_name = csv_to_xls(file_path)
                filename = str(filename.split(".csv")[0]) + ".xls"
            else:
                file_path_name = file_path
            file_list.append(file_path_name)
            if not file_upload:
                self.write_recorde(file_path_name, filename)
        return file_list

    def write_recorde(self, file_path, filename):
        # print filename
        serial_number = "-".join(filename.split("-")[:2])
        write_dict = {"filename":filename, "file_path": file_path, "serial_number":serial_number}
        try:
            statue = UploadFileRecorde.objects.filter(filename=filename,file_path=file_path)
        except Exception, e:
            log.info(str(e))
            statue = []
        if statue:
            print "文件记录已经存在!"
            log.info("文件: %s 已经存在" % filename)
            return
        ufr = UploadFileRecorde(**write_dict)
        try:
            ufr.save()
        except Exception,e:
            log.info(str(e))
        try:
            time.sleep(1)
            StatementViewImport([filename]).import_files_to_statement_view()
        except Exception, e:
            log.info(str(e))
            update_file_statue(filename, 0, error_msg=str(e))



class InventoryUpload(object):
    def __init__(self, fileobj_list):
        self.fileobj_list = fileobj_list


    def write_file(self, file_upload=None):
        file_list = []
        for fileobj in self.fileobj_list:
            filename = fileobj.name.replace(" ", "")
            file_path = os.path.join(get_path(UPLOAD_PATH), filename)
            with open(file_path, "wb+") as f:
                for chunk in fileobj.chunks():
                    f.write(chunk)
            file_list.append(file_path)
            if not file_upload:
                print "1"*100
                self.write_recorde(file_path, filename)
        return file_list

    def write_recorde(self, file_path, filename):
        # print filename
        write_dict = {"filename": filename, "file_path": file_path}
        try:
            statue = InventoryUploadRecorde.objects.filter(filename=filename, file_path=file_path)
        except Exception, e:
            log.info(str(e))
            statue = []
        if statue:
            print "文件记录已经存在!"
            log.info("文件: %s 已经存在" % filename)
            return
        ufr = InventoryUploadRecorde(**write_dict)
        try:
            ufr.save()
        except Exception, e:
            log.info(str(e))
        try:
            time.sleep(1)
            #StatementViewImport([filename]).import_files_to_statement_view()
            InventoryReportImport([filename]).import_file()
        except Exception, e:
            log.info(str(e))
            update_file_statue(filename, 0, error_msg=str(e))




def inventory_list_files(**params):
    file_list = InventoryUploadRecorde.objects.filter().values()
    return list(file_list)[::-1]



def list_files(params):
    pageSize = params.get("pageSize", "10")
    pageNumber = params.get("pageNumber", "1")
    searchText = params.get("searchText","")
    if int(pageSize) < 0:
        pageSize = 12
    else:
        pageSize = int(pageSize)
    if int(pageNumber) < 1:
        pageNumber = 1
    else:
        pageNumber = int(pageNumber)

    query_select = Q()
    if searchText:
        try:
            query_select = query_select &Q(id=int(searchText))
        except Exception, e:
            query_select = query_select &(Q(filename=searchText)| Q(serial_number=searchText))
    else:
        query_select = query_select
    file_list = UploadFileRecorde.objects.filter(query_select).order_by("-id").values()[(pageNumber - 1) * pageSize: pageNumber * pageSize]
    total = UploadFileRecorde.objects.filter(query_select).count()
    return  {"rows": list(file_list)[::-1], "total": total}




def delete_file(ids, inventory=None):
    statue = 0
    log.info("delete filename: %s" % ids)
    msg = ""
    if inventory:
        id_list = ids
        try:
            file_list = InventoryUploadRecorde.objects.filter(id__in=id_list).values_list("filename",flat=True)
            file_path_list = InventoryUploadRecorde.objects.filter(id__in=id_list).values_list("file_path",flat=True)
            if file_list and file_path_list:
                InventoryReportsData.objects.filter(filename__in=file_list).delete()
                InventoryUploadRecorde.objects.filter(id__in=id_list).delete()
            for file_path in file_path_list:
                os.remove(file_path)
        except Exception, e:
            log.info(" delete inventory file error: %s" %(e))
            msg = str(e)
            statue = -1
            if "No such file or directory:" in str(e):
                InventoryUploadRecorde.objects.filter(filename=filename).delete()
    else:
        id_list = ids #删除上传记录的时候，传递的是id列表
        try:
            file_list = UploadFileRecorde.objects.filter(id__in=id_list).values_list("filename",flat=True)
            file_path_list = UploadFileRecorde.objects.filter(id__in=id_list).values_list("file_path",flat=True)
            if file_list and file_path_list:
                StatementView.objects.filter(filename__in=file_list).delete()
                UploadFileRecorde.objects.filter(id__in=id_list).delete()
            for file_path in file_path_list:
                os.remove(file_path)
        except Exception, e:
            log.info(" delete file error: %s " % (e))
            msg = str(e)
            statue = -1
            if "No such file or directory:" in str(e):
                #UploadFileRecorde.objects.filter(filename=filename).delete()
                UploadFileRecorde.objects.filter(id__in=filename).delete()
    return {"statue": statue, "msg": msg }




def download_file(filename, inventory_file=None):
    if inventory_file:
        try:
            the_file_name = InventoryUploadRecorde.objects.filter(filename=filename).values_list("file_path", flat=True)[0]
        except Exception, e:
            the_file_name = ""
    else:
        try:
            the_file_name = UploadFileRecorde.objects.filter(filename=filename).values_list("file_path",flat=True)[0]
        except Exception, e:
            the_file_name = ""

    if os.path.exists(the_file_name):
        return the_file_name
    else:
        return ""






def get_path(root_path):
    one_p_num = 1000
    two_p_num = 200
    i, j= 0, 0
    while True:
        one_path = os.path.join(root_path, str(i))
        if not os.path.exists(one_path):
            os.mkdir(one_path)
        if len(os.listdir(one_path)) >= one_p_num:
            i += 1
            one_path = os.path.join(root_path, str(i))
            if not os.path.exists(one_path):
                os.mkdir(one_path)
            else:
                continue
        else:
            two_path = os.path.join(one_path, str(j))
            if not os.path.exists(two_path):
                os.mkdir(two_path)
            if len(os.listdir(two_path)) >= two_p_num:
                j+= 1
            else:
                return two_path
