#encoding:utf-8
from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
            url(r'^$', 'manageApp.views.home', name='home'),
            url(r'^user-login/$', 'manageApp.views.login', name='login'),
            url(r'^user-logout/$', 'manageApp.views.logout', name='logout'),

            url(r'^files-list/$', 'manageApp.views.files_action', name='files_list'),
            url(r'^list-files-json/$', 'manageApp.views.list_fils_json', name='list_fils_json'),
                       )