# encoding:utf-8

from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib import  auth
from django.contrib.auth.decorators import login_required

from manageApp.dataService.upload_file import FileUpload

# Create your views here.




# @login_required(login_url="/manage/user-login/")
@login_required(login_url='/manage/user-login/')
def home(request):
    username = request.user.username
    if request.method == "POST":
        ufiles = request.FILES.getlist("file[]", "")
        upload_files = FileUpload(ufiles,username=username).write_file()
        print upload_files
    return  render(request, 'manage_index.html', locals())


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect("/manage/")
        else:
            return render(request, 'login.html', locals())
    else:
        print "run login ..."
        return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")




