# encoding:utf-8
import  time
import  os
from django.conf import  settings
from manageApp.models import  UploadFileRecorde, StatementView, InventoryUploadRecorde
from manageApp.dataService.dataImport import  StatementViewImport, InventoryReportImport
from manageApp.dataService.tasks_util import update_file_statue
from center.models import InventoryReportsData
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
            file_list.append(file_path)
            if not file_upload:
                self.write_recorde(file_path, filename)
        return file_list

    def write_recorde(self, file_path, filename):
        # print filename
        write_dict = {"filename":filename, "file_path": file_path}
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



def list_files(**params):
    file_list = UploadFileRecorde.objects.filter().values()
    return  list(file_list)[::-1]
    tmp_file_list = []
    for fn in file_list:
        tmp_dict = {}
        tmp_dict["filename"] = fn.filename.split("__")[-1]
        tmp_dict["file_path"] = fn.file_path
        tmp_dict["upload_date"] = fn.uploadtime
        tmp_file_list.append(tmp_dict)
    return list(tmp_file_list)[::-1]




def delete_file(filename, inventory=None):
    statue = 0
    # print  "filename:", filename
    log.info("delete filename: %s" % filename)
    msg = ""
    if inventory:
        try:
            InventoryReportsData.objects.filter(filename=filename).delete()
            ffile = InventoryUploadRecorde.objects.filter(filename=filename)
            file_path = ffile[0].file_path
            os.remove(file_path)
            ffile.delete()
        except Exception ,e:
            log.info("删除文件失败: %s" %(str(e)))
            msg = str(e)
            statue = -1
            if "No such file or directory:" in str(e):
                InventoryUploadRecorde.objects.filter(filename=filename).delete()
        pass
    else:
        try:
            StatementView.objects.filter(filename=filename).delete()
            ffile= UploadFileRecorde.objects.filter(filename=filename)
            file_path = ffile[0].file_path
            os.remove(file_path)
            ffile.delete()
        except Exception, e:
            # print "delete file error: %s" %(e)
            log.info(" delete file error: %s " % (e))
            msg = str(e)
            statue = -1
            if "No such file or directory:" in str(e):
                UploadFileRecorde.objects.filter(filename=filename).delete()
    return {"statue": statue, "msg": msg }










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