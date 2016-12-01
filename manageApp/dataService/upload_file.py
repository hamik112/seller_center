# encoding:utf-8
import  time
import  os
from django.conf import  settings
from manageApp.models import  UploadFileRecorde


UPLOAD_PATH = settings.UPLOAD_PATH

class FileUpload(object):
    def __init__(self, fileobj_list, username=None):
        self.fileobj_list = fileobj_list
        self.username = username

    def __call__(self, *args, **kwargs):
        return self.write_file()

    def write_file(self):
        file_list = []
        for fileobj in self.fileobj_list:
            fname = fileobj.name.replace(" ", "")
            if self.username:
                filename = str(self.username) +"__"+ str(time.time()).replace(".","")+"__" + fname
            else:
                filename = str(time.time()).replace(".","")+"_" + fname
            file_path = os.path.join(UPLOAD_PATH, filename)
            with open(file_path, "wb+") as f:
                for chunk in fileobj.chunks():
                    f.write(chunk)
            file_list.append(file_path)
            self.write_recorde(file_path, filename)
        return file_list

    def write_recorde(self, file_path, filename):
        print filename
        write_dict = {"filename":filename, "file_path": file_path}
        ufr = UploadFileRecorde(**write_dict)
        try:
            ufr.save()
        except Exception,e:
            print e




def list_files(**params):

    file_list = UploadFileRecorde.objects.filter().values()
    return  list(file_list)
    tmp_file_list = []
    for fn in file_list:
        tmp_dict = {}
        tmp_dict["filename"] = fn.filename.split("__")[-1]
        tmp_dict["file_path"] = fn.file_path
        tmp_dict["upload_date"] = fn.uploadtime
        tmp_file_list.append(tmp_dict)
    return list(tmp_file_list)



def delete_file(filename):
    statue = 0
    msg = ""
    try:
        ffile= UploadFileRecorde.objects.filter(filename=filename)
        file_path = ffile[0].file_path
        os.remove(file_path)
        ffile.delete()
    except Exception, e:
        print "delete file error: %s" %(e)
        msg = str(e)
        statue = -1
    return {"statue": statue, "msg": msg }