# encoding:utf-8

import  json
import  logging

from django.contrib import  auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import StreamingHttpResponse
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from SellerCenter.utils import json_encode
from center.dataService.data_format import file_iterator
from manageApp.dataService.JSON_serial import json_serial
from manageApp.dataService.dataImport import  StatementViewImport, InventoryReportImport
from manageApp.dataService.dataImport import get_update_error_str
from manageApp.dataService.deal_order import write_file_other_handle,write_file_other_handle2
from manageApp.dataService.filename_to_storename import FilenameStoreName
from manageApp.dataService.upload_file import FileUpload, list_files, delete_file, download_file
from manageApp.dataService.upload_file import InventoryUpload, inventory_list_files
from manageApp.models import FileUploadOther

log = logging.getLogger("django.request")



def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect("/manage/files-list/")
        else:
            return render(request, 'login.html', locals())
    else:
        print "run login ..."
        log.info("run login ...")
        return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")



# @login_required(login_url="/manage/user-login/")
@login_required(login_url='/manage/user-login/')
@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login/")
def home(request):
    username = request.user.username
    if request.method == "POST":
        ufiles = request.FILES.getlist("file[]", "")
        # print ufiles
        log.info(ufiles)
        upload_files = FileUpload(ufiles,username=username).write_file()
        return HttpResponse(json.dumps(upload_files))
    return  render(request, 'manage_index.html', locals())

@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login/")
@login_required(login_url="/manage/user-login/")
def files_action(request):
    username = request.user.username
    if request.method == "POST":
        if request.POST.get("action_type", "") == "delete":
            #filename =  request.POST.get("filename", "")
            inventory = request.POST.get("inventory", "")
            id_list = request.POST.getlist("ids[]", [])
            print id_list
            if id_list and inventory:
                result = delete_file(id_list, inventory)
            else:
                result = delete_file(id_list)                
            return HttpResponse(json.dumps(result))
        elif request.POST.get("action_type", "") == "update_statement":
            filename = request.POST.get("filename", "")
            result = StatementViewImport([filename]).import_files_to_statement_view()
            result = result[0]
            return HttpResponse(json.dumps(result))
        elif request.POST.get("action_type", "") == "update_report":
            filename = request.POST.get("filename", "")
            result =InventoryReportImport([filename]).import_file()
            result = result[0]
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps({"statue": -1, "msg":""}))
    else:
        return render(request, "file_list.html", locals())


@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login/")
@login_required(login_url="/manage/user-login/")
def list_fils_json(request):
    #files_list = list_files(**{"pageSize":pageSize, "pageNumber":pageNumber})
    files_list = list_files(request.GET)
    return HttpResponse(json.dumps(files_list, default=json_serial))



@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def filename_to_storename(request):
    username = request.user.username
    if request.method == "POST":
        fsn = FilenameStoreName()
        if request.POST.get("action_type","") == "delete":
            result = fsn.post_delete_line(request.POST)
            return HttpResponse(json.dumps(result, default=json_serial))
        elif request.POST.get("action_type", "") == "add":
            result = fsn.post_add_line(request.POST)
            return HttpResponse(json.dumps(result, default=json_serial))
        elif request.POST.get("action_type", "") == "update":
            log.info("update ...")
            result = fsn.post_update_line(request.POST)
            return HttpResponse(json.dumps(result, default=json_serial))
        elif request.POST.get("action_type", "") == "file_storename":
            log.info("file to storename ...")
            ufiles = request.FILES.getlist("filename", "")
            result = fsn.post_add_many_line(ufiles,username , request.POST)
            return HttpResponse(json.dumps(result, default=json_serial))
        return render(request,"filename_to_storename.html", locals())
    else:
        return render(request, 'filename_to_storename.html', locals())


@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def ajax_download_filename(request):
    filename = request.GET.get("filename", "")
    print "filename: ", filename
    download_report = request.GET.get("download_report", "")  #下载上传的report文件
    if download_report:
        the_file_name = download_file(filename,inventory_file=True)
    else:
        the_file_name = download_file(filename)                   #在数据库找到文件上传的绝对路径

    if download_report and not  the_file_name:
        return HttpResponseRedirect("/manage/inventory-report-import/")
    if not the_file_name:
        return HttpResponseRedirect("/manage/files-list/")
    print the_file_name
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"'%str(filename)
    return response




@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def filename_to_token(request):
    log.info("file to token ...")
    username = request.user.username
    if request.method == "POST":
        ufiles = request.FILES.getlist("filename", "")
        fsn = FilenameStoreName()
        result = fsn.upload_token(ufiles, username, request.POST)
        return HttpResponse(json.dumps(result, default=json_serial))
    else:
        log.info("file to token method error...")
        return HttpResponse(json.dumps({"status":"-1","msg":"method error!"}))



@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def filename_to_storename_json(request):
    result = FilenameStoreName().read_data(request.GET)
    return HttpResponse(json.dumps(result, default=json_serial))


@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def get_update_error_msg(request):
    uid = request.GET.get("uid", "")
    error_msg = get_update_error_str(uid)
    result = {"statue": 0, "msg": error_msg}
    return HttpResponse(json.dumps(result))

@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
@csrf_exempt
def inventory_import(request):
    if request.method == "POST":
        files_list = inventory_list_files()
        return HttpResponse(json.dumps(files_list, default=json_serial))
    return render(request, "inventory_report_import.html", locals())


@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def inventory_import_upload(request):
    if request.method == "POST":
        ufiles = request.FILES.getlist("file[]", "")
        upload_files = InventoryUpload(ufiles).write_file()
        return HttpResponse(json.dumps(upload_files))
    else:
        return render(request, "inventory_report_upload.html", locals())

@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def other_handle_import(request):
    if request.method == "POST":
        print "post"
        ufiles = request.FILES.getlist("file[]", "")
        try:
            write_file_other_handle(ufiles)
        except Exception,e:
            print str(e)
            return HttpResponse(0)
        return HttpResponse(1)
    else:
        print "get"
        return render(request, "other_handle_import.html", locals())


@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def other_handle_upload(request):
    return render(request, "other_handle_upload.html", locals())

@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def other_handle_upload_data(request):
    params = request.GET.copy()
    objs = FileUploadOther.objects.filter(type=0).order_by('-id')
    pageSize = params.get("pageSize", "10")
    pageNumber = params.get("pageNumber", "1")
    searchText = params.get("searchText", "")
    if int(pageSize) < 0:
        pageSize = 12
    else:
        pageSize = int(pageSize)
    if int(pageNumber) < 1:
        pageNumber = 1
    else:
        pageNumber = int(pageNumber)

    if searchText:
        objs = objs.filter(file_name__icontains=searchText)
    try:
        return HttpResponse(json_encode({"rows":objs[(pageNumber - 1) * pageSize: pageNumber * pageSize], "total":objs.count()}))
    except Exception,e:
        print str(e)
        return HttpResponse()

@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def other_handle_ajax_upload(request):
    file_id = request.POST.get('fileid')
    obj = FileUploadOther.objects.get(id=file_id)
    response = StreamingHttpResponse(file_iterator(obj.file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % str(obj.file_name)
    return response

@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def other_handle_file_delet(request):
    post_dict = request.POST.copy()
    dele_id = post_dict.getlist("ids[]", "")
    try:
        FileUploadOther.objects.filter(id__in=dele_id).delete()
        return HttpResponse(1)
    except Exception,e:
        return HttpResponse(0)

@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def other_handle_import2(request):
    if request.method == "POST":
        print "post"
        ufiles = request.FILES.getlist("file[]", "")
        try:
            write_file_other_handle2(ufiles)
        except Exception,e:
            print str(e)
            return HttpResponse(0)
        return HttpResponse(1)
    else:
        print "get"
        return render(request, "other_handle_import2.html", locals())

@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def other_handle_upload2(request):
    if request.method == "POST":
        params = request.GET.copy()
        objs = FileUploadOther.objects.filter(type=2).order_by('-id')
        pageSize = params.get("pageSize", "10")
        pageNumber = params.get("pageNumber", "1")
        searchText = params.get("searchText", "")
        if int(pageSize) < 0:
            pageSize = 12
        else:
            pageSize = int(pageSize)
        if int(pageNumber) < 1:
            pageNumber = 1
        else:
            pageNumber = int(pageNumber)

        if searchText:
            objs = objs.filter(file_name__icontains=searchText)
        try:
            return HttpResponse(
                json_encode({"rows": objs[(pageNumber - 1) * pageSize: pageNumber * pageSize], "total": objs.count()}))
        except Exception, e:
            print str(e)
            return HttpResponse()
    else:
        return render(request, "other_handle_upload2.html", locals())

@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def other_handle_ajax_upload2(request):
    file_id = request.POST.get('fileid')
    obj = FileUploadOther.objects.get(id=file_id)
    response = StreamingHttpResponse(file_iterator(obj.file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % str(obj.file_name)
    return response

@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def other_handle_file_delet2(request):
    post_dict = request.POST.copy()
    dele_id = post_dict.getlist("ids[]", "")
    try:
        FileUploadOther.objects.filter(id__in=dele_id).delete()
        return HttpResponse(1)
    except Exception,e:
        return HttpResponse(0)