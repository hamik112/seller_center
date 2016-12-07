#!/usr/bin/env python
# encoding:utf-8

from django.contrib.auth.models import User
from manageApp.models import  FilenameToStorename



def user_add(update=None, **parmas):
    print parmas, update
    statue ,msg = 0, ""
    if update:
        try:
            print "update user ..."
            user = User.objects.filter(username=parmas.get("email", ""))[0]
            user.set_password(parmas.get("password",""))
        except Exception, e:
            msg = u"没有找到该用户email"
            statue = -1
    else:
        try:
            User.objects.create_user(username=parmas.get("email", ""),
                                     email=parmas.get("email", ""),
                                     password=parmas.get("password"))
        except Exception, e:
            print str(e)
            msg = str(e)
            statue = -1
    return statue,msg

def user_del(**params):
    email = params.get("email", "")
    statue, msg = 0, ""
    try:
        User.objects.filter(username=email).delete()
    except Exception, e:
        msg = str(e)
        statue = -1
    return statue, msg


class FilenameStoreName(object):
    def __init__(self):
        pass

    def read_data(self):
        file_store_list = FilenameToStorename.objects.filter()
        return list(file_store_list.values())

    def read_one(self, read_id):
        try:
            id_data = FilenameToStorename.objects.filter(id=read_id).values()[0]
        except Exception, e:
            id_data = {}
        return id_data

    def add_line(self, update=None, **params):
        print "update: ",update
        fts = FilenameToStorename(**params)
        statue, msg = 0, ""
        try:
            fts.save()
            statue, msg = user_add(update=update, **params)
        except Exception, e:
            try:
                FilenameToStorename.objects.filter(email=params.get("email","")).update(**params)
                statue, msg = user_add(update=update,**params)
            except Exception,e:
                statue = -1
                msg = ""
                print e
        return {"statue": statue, "msg": msg}

    def delete_line(self, **parmas):
        dele_id = parmas.get("dele_id", "")
        statue, msg = 0, ""
        try:
            fts = FilenameToStorename.objects.filter(id=dele_id)
            email = fts.values("email")[0]
            fts.delete()
            statue, msg = user_del(**email)
        except Exception, e:
            statue = -1
        return {"statue": statue, "msg": msg}



    def post_add_line(self, post_dict):
        print post_dict
        keys_list = ["serial_number", "storename", "email", "password"]
        params_dict = {}.fromkeys(keys_list, "")
        for name in keys_list:
            params_dict[name] = post_dict.get(name, "").strip()
        if post_dict.get("is_update") == "update":
            result = self.add_line(update=True, **params_dict)
        else:
            print "add ............"
            result = self.add_line(**params_dict)
        return  result

    def post_delete_line(self, post_dict):
        dele_id = post_dict.get("dele_id", "")
        print dele_id
        return self.delete_line(**{"dele_id":dele_id})

    def post_update_line(self, post_dict):
        update_id = post_dict.get("update_id", "")
        infos = self.read_one(update_id)
        return {"statue":0, "infos": infos }


