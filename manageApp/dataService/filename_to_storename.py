#!/usr/bin/env python
# encoding:utf-8

import  datetime
import pytz

from django.contrib.auth.models import User
from django.db.models import Q
from manageApp.models import  FilenameToStorename, StoreKeys, InventoryUploadRecorde
from manageApp.dataService.upload_file import FileUpload
from manageApp.dataService.deal_xls import read_xls


import  logging
log = logging.getLogger("scripts")


def user_add(update=None, **parmas):
    print parmas, update
    statue ,msg = 0, ""
    if update:
        try:
            # print "update user ..."
            log.info("update user ...")
            user = User.objects.filter(username=parmas.get("email", ""))[0]
            user.set_password(parmas.get("password",""))
        except Exception, e:
            msg = u"没有找到该用户email"
            log.error("没有找到改用户email")
            statue = -1
    else:
        try:
            User.objects.create_user(username=parmas.get("email", ""),
                                     email=parmas.get("email", ""),
                                     password=parmas.get("password", ""))
        except Exception, e:
            # print str(e)
            log.info(str(e))
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
        log.info(msg)
        statue = -1
    return statue, msg


class FilenameStoreName(object):
    def __init__(self):
        pass

    def read_data(self, params):
        pageSize = params.get("pageSize", "10")
        pageNumber = params.get("pageNumber", "1")
        searchText = params.get("searchText", "")
        #query_select = Q()
        if int(pageSize) < 0:
            pageSize = 1
        else:
            pageSize = int(pageSize)
        if int(pageNumber) < 1:
            pageNumber = 1
        else:
            pageNumber = int(pageNumber)
        query_select = Q()
        if searchText:
            try:
                query_select = query_select & Q(id=int(searchText))
            except Exception, e:
                query_select = query_select & (Q(filename=searchText) | 
                                               Q(serial_number = searchText) |
                                               Q(gateway_name = searchText) | 
                                               Q(storename = searchText) | 
                                               Q(manager= searchText) |
                                               Q(email = searchText) | 
                                               Q(really_store=searchText)
                                               )
        else:
            query_select = query_select
        file_store_list = FilenameToStorename.objects.filter(query_select)[(pageNumber - 1) * pageSize:pageNumber * pageSize]
        total = FilenameToStorename.objects.filter(query_select).count()
        return_file_store_list = []
        for i in xrange(file_store_list.count()):
            tmp_dict = file_store_list.values()[i]
            tmp_dict["has_token"] = self.judge_has_token(tmp_dict.get("email"),tmp_dict.get("gateway_name"))
            return_file_store_list.append(tmp_dict)
        return {"rows":list(return_file_store_list), "total":total}


        # return list(file_store_list.values())
    def judge_has_token(self, email, gateway_name):
        token, has_key = "",""
        try:
            token = StoreKeys.objects.filter(email=email,storename=gateway_name).values("mws_authtoken")
        except Exception, e:
            token = ""
        if token:
            has_key = "1"
        else:
            has_key = "0"
        return has_key


    def read_one(self, read_id):
        try:
            id_data = FilenameToStorename.objects.filter(id=read_id).values()[0]
        except Exception, e:
            id_data = {}
        return id_data

    def add_line(self, update=None, **params):
        # print "update: ",update
        fts = FilenameToStorename(**params)
        statue, msg = 0, ""
        params["password"] = "starmerx"
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
                log.info(str(msg))
                # print e
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
            log.info(str(e))
            statue = -1
        return {"statue": statue, "msg": msg}



    def post_add_line(self, post_dict, keys_list=None):
        if keys_list:
            keys_list = keys_list
        else:
            keys_list = ["serial_number", "storename", "email","password" ,"manager", "payment_time"]
        params_dict = {}.fromkeys(keys_list, "")
        for name in keys_list:
            params_dict[name] = str(post_dict.get(name, "")).strip()
        if post_dict.get("is_update") == "update":
            result = self.add_line(update=True, **params_dict)
        else:
            # print "add ............"
            log.info(" add one line ...")
            result = self.add_line(**params_dict)
        return  result

    def post_delete_line(self, post_dict):
        dele_id = post_dict.getlist("dele_id[]", "")
        log.info(" delete id: %s" % str(dele_id))
        success_list, error_list = [], []
        for did in dele_id:
            status = self.delete_line(**{"dele_id": did})
            print "1"*100
            print "status:", status
            if status.get("statue",0) == "-1" or status.get("statue", 0) == -1:
                error_list.append(status)
            else:
                success_list.append(status)
        if len(success_list) == 0:
            if not error_list: 
                error_list = [{"msg":"删除错误!"}]
            msg = error_list[0].get("msg", "")
            status = -1
        else:
            status = 0
            msg = "成功了%s条，失败了%s条"%(str(len(success_list)),str(len(error_list)))
        return {"statue":status, "msg": msg}
        #return self.delete_line(**{"dele_id":dele_id})

    def post_update_line(self, post_dict):
        update_id = post_dict.get("update_id", "")
        infos = self.read_one(update_id)
        return {"statue":0, "infos": infos }


    def post_add_many_line(self, ufils, username ,post_dict):
        """ 批量导入对应关系 """
        fud_name = FileUpload(ufils,username=username).write_file(file_upload=True)
        need_header_list = [u"序号",u"网关代码", u"店名", u"legal人名",u"账号email",
            u"新富国银行卡",u"KDT",u"未更换老富国卡", u"卖家ID", u"亚马逊Key ID",
            u"亚马逊密钥",u"真假", u"时间"]
        value_list = ["serial_number", "gateway_name","storename", "manager" , "email",
                      "new_card","kdt_card","old_card","seller_id", "amazon_key_id",
                      "amazon_key","really_store","payment_time"]
        key_value_dict = dict(zip(need_header_list, value_list))
        try:
            _value_list = read_xls(fud_name[0])
            data = _value_list.get("data",[])[0].get("values",[])
        except Exception,e :
            log.info( str(e))
            return {"statue": -1, "msg": "上传文件失败/文件的sheet不是第一个!"}
        header_list  = data[0]
        header_dict = {}.fromkeys(need_header_list, "")
        for name in need_header_list:
            try:
                header_dict[name] = header_list.index(name)
            except Exception, e:
                msg = "没有找到字段: %s" % str(name)
                log.error(str(msg))
                return {"statue":-1, "msg": msg}
        n, error_list = 0, []
        for line in data[1:]:
            if "".join([str(i) for i in line]) == "": continue
            tmp_dict = {}
            for name in need_header_list:
                try:
                    tmp_dict[key_value_dict.get(name)] = line[header_dict.get(name)]
                except Exception, e:
                    print str(e)
                    error_list.append(str(n) + str(line))
                    n += 1
                    continue
                if not line[header_dict.get(name)]:
                    error_list.append(str(n)+":"+str(line) )
                    n +=1
                    continue
            tmp_dict["password"] = "starmerx"
            if str(tmp_dict["payment_time"]) == "42":
                tmp_dict["payment_time"] = ""
            else:
                tmp_dict["payment_time"] = str(getdate(tmp_dict.get("payment_time", "")))
            if tmp_dict["really_store"] == u"假" or tmp_dict["really_store"] == "假":
                tmp_dict["really_store"] = "0"

            if tmp_dict["serial_number"] == "" or tmp_dict["gateway_name"] == "" or tmp_dict["email"] == "":
                error_list.append(str(n) + ":" + str(line))
                n += 1
                continue
            # if "" in tmp_dict.values():
            #     continue
            self.post_add_line(tmp_dict, keys_list=value_list)
        if len(error_list) > 0:
            msg = "还有 %s 没有添加!" % (str(n))
        else:
            msg = "所有都已经添加完成"
        log.info(str(msg))
        return {"statue":0, "msg": msg}


    def upload_token(self, ufils,username, post_dict):
        msg = ""
        fud_name = FileUpload(ufils,username=username).write_file(file_upload=True)
        need_header_list = ["name", "ACCESS KEY","SECRET KEY","ACCOUNT ID",	"MKPLACEID", "MWSAuthToken"]
        value_list = ["storename", "access_key", "secret_key", "account_id", "mkplaceid", "mws_authtoken"]
        key_value_dict = dict(zip(need_header_list, value_list))
        try:
            _value_list = read_xls(fud_name[0])
            data = _value_list.get("data",[])[0].get("values",[])
        except Exception,e :
            log.info( str(e))
            return {"statue": -1, "msg": "上传文件失败/文件的sheet不是第一个!"}
        header_list  = data[0]
        header_dict = {}.fromkeys(need_header_list, "")
        for name in need_header_list:
            try:
                header_dict[name] = header_list.index(name)
            except Exception, e:
                msg = "没有找到字段: %s" % str(name)
                log.error(str(msg))
                return {"statue":-1, "msg": msg}
        n, error_list = 1, []
        for line in data[1:]:
            tmp_dict = {}
            for name in need_header_list:
                try:
                    tmp_dict[key_value_dict.get(name)] = line[header_dict.get(name)]
                except Exception, e:
                    print str(e)
                    error_list.append(str(n) + str(line))
                    continue
                if not line[header_dict.get(name)]:
                    error_list.append(str(n)+":"+str(line) )
                    continue
            tmp_dict["email"] = self.get_storename_email(tmp_dict.get("storename"))   #这个，应该是网关名字
            if "" in tmp_dict.values():
                error_list.append(str(n) + ":" + str(line))
                continue
            try:
                stk = StoreKeys(**tmp_dict)
                stk.save()

            except Exception ,e:
                log.error(str(e))
                try:
                    StoreKeys.objects.filter(mws_authtoken=tmp_dict.get("mws_authtoken")).update(**tmp_dict)
                except Exception, e:
                    log.error(str(e))
                    error_list.append(str(n)+":"+str(line))
        if len(error_list) > 0:
            msg = "还有 %s 没有添加!" % (str(len(error_list)))
        else:
            msg = "所有都已经添加完成"
        log.info(str(msg))
        return {"status":0, "msg": msg}

    def get_storename_email(self,storename):
        try:
            #email = FilenameToStorename.objects.get(storename=storename).email
            email = FilenameToStorename.objects.get(gateway_name=storename).email
        except Exception, e:
            email = ""
        return email





def getdate(x, tz=None):
    """
    convert Gregorian float of the date , preserving hours, minutes,
    seconds and microseconds. return value is a datetime
    """
    __s_date = datetime.date(1899, 12, 31).toordinal() - 1
    if tz is None: tz = pytz._UTC()
    ix = int(x)
    dt = datetime.datetime.fromordinal(ix + __s_date)
    remainder = float (x) - ix
    hour, remainder = divmod(24*remainder, 1)
    minute, remainder = divmod(60*remainder, 1)
    second, remainder = divmod(60*remainder, 1)
    microsecond = int(1e6*remainder)
    if microsecond<10: microsecond=0 # compensate for rounding errors
    dt = datetime.datetime(
        dt.year, dt.month, dt.day, int(hour), int(minute), int(second),
        microsecond, tzinfo=pytz.utc).astimezone(tz)
    if microsecond>999990: # compensate for rounding errors
        dt += datetime.timedelta(microseconds=1e6-microsecond)
    return dt

