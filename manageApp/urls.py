#encoding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
            url(r'^$', 'manageApp.views.home', name='home'),
            url(r'^user-login/$', 'manageApp.views.login', name='login'),
            url(r'^user-logout/$', 'manageApp.views.logout', name='logout'),

            url(r'^files-list/$', 'manageApp.views.files_action', name='files_list'),
            url(r'^list-files-json/$', 'manageApp.views.list_fils_json', name='list_fils_json'),
            url(r'^filename-to-storename/$', 'manageApp.views.filename_to_storename', name='filename_to_storename'),
            url(r'^filename-to-token/$', 'manageApp.views.filename_to_token', name='filename_to_token'),
            url(r'^filename-to-storename-json/$', 'manageApp.views.filename_to_storename_json', name="filename_to_storename_json"),
            url(r'^get-update-error-msg/$', 'manageApp.views.get_update_error_msg', name="get_update_error_msg"),
            url(r'^inventory-report-import/$', 'manageApp.views.inventory_import', name="inventory_import"),

                       )

urlpatterns += patterns('',
                        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.STATICFILES_DIRS[1],
                            }),
                        )

