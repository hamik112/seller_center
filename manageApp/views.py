# encoding:utf-8

import  json
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User
from django.contrib import  auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from manageApp.dataService.upload_file import FileUpload, list_files, delete_file
from manageApp.dataService.deal_xls import read_xls
from manageApp.dataService.JSON_serial import json_serial
from manageApp.dataService.dataImport import  StatementViewImport

from manageApp.dataService.filename_to_storename import FilenameStoreName
from manageApp.dataService.dataImport import get_update_error_str
# Create your views here.

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
        print ufiles
        upload_files = FileUpload(ufiles,username=username).write_file()
        return HttpResponse(json.dumps(upload_files))
    return  render(request, 'manage_index.html', locals())

@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login/")
@login_required(login_url="/manage/user-login/")
def files_action(request):
    username = request.user.username
    if request.method == "POST":
        if request.POST.get("action_type", "") == "delete":
            filename =  request.POST.get("filename", "")
            result = delete_file(filename)
            return HttpResponse(json.dumps(result))
        elif request.POST.get("action_type", "") == "update_statement":
            filename = request.POST.get("filename", "")
            result = StatementViewImport([filename]).import_files_to_statement_view()
            result = result[0]
            return HttpResponse(json.dumps(result))

        else:
            return HttpResponse(json.dumps({"statue": -1, "msg":""}))
    else:
        return render(request, "file_list.html", locals())


@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login/")
@login_required(login_url="/manage/user-login/")
def list_fils_json(request):
    files_list = list_files()
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
            print "update ..........."
            result = fsn.post_update_line(request.POST)
            return HttpResponse(json.dumps(result, default=json_serial))
        elif request.POST.get("action_type", "") == "file_storename":
            print "file to storename ..."
            ufiles = request.FILES.getlist("filename", "")
            print ufiles
            result = fsn.post_add_many_line(ufiles,username , request.POST)
            return HttpResponse(json.dumps(result, default=json_serial))
        return render(request,"filename_to_storename.html", locals())
    else:
        return render(request, 'filename_to_storename.html', locals())


@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def filename_to_storename_json(request):
    result = FilenameStoreName().read_data()
    return HttpResponse(json.dumps(result, default=json_serial))


@user_passes_test(lambda u:u.is_staff, login_url="/manage/user-login")
@login_required(login_url="/manage/user-login")
def get_update_error_msg(request):
    uid = request.GET.get("uid", "")
    error_msg = get_update_error_str(uid)
    result = {"statue": 0, "msg": error_msg}
    return HttpResponse(json.dumps(result))