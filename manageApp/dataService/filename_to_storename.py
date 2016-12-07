#!/usr/bin/env python
# encoding:utf-8

from django.contrib.auth.models import User
from manageApp.models import  FilenameToStorename


def user_add(update=None, **parmas):
    statue ,msg = 0, ""
    if update:
        try:
            user = User.objects.filter(username=parmas.get("email", ""))[0]
            user.set_password(parmas.get("password",""))
        except Exception, e:
            msg = u"没有找到该用户email"
            statue = -1
    else:
        user = User()
        user.username = parmas.get("email", "")
        user.email = parmas.get("email", "")
        user.set_password(parmas.get("passwrod"))
        try:
            user.save()
        except Exception, e:
            msg = str(e)
            statue = -1
    return statue,msg


class FilenameStoreName(object):
    def __init__(self):
        pass

    def read_data(self):
        file_store_list = FilenameToStorename.objects.filter()
        return list(file_store_list.values())

    def read_one(self, read_id):
        return FilenameToStorename.objects.filter(id=read_id).values()[0]

    def add_line(self, **params):
        fts = FilenameToStorename(**params)
        statue, msg = 0, ""
        try:
            fts.save()
            statue, msg = user_add(**params)
        except Exception, e:
            try:
                FilenameToStorename.objects.filter(email=params.get("email","")).update(**params)
                statue, msg = user_add(update=True,**params)
            except Exception,e:
                statue = -1
                msg = ""
                print e
        return {"statue": statue, "msg": msg}

    def delete_line(self, **parmas):
        dele_id = parmas.get("dele_id", "")
        statue, msg = 0, ""
        try:
            FilenameToStorename.objects.filter(id=dele_id).delete()
        except Exception, e:
            statue = -1
        return {"statue": statue, "msg": msg}



    def post_add_line(self, post_dict):
        keys_list = ["serial_number", "storename", "email", "password"]
        params_dict = {}.fromkeys(keys_list, "")
        for name in keys_list:
            params_dict[name] = post_dict.get(name, "").strip()
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


