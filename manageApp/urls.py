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
            url(r'^ajax-download-filename/$', 'manageApp.views.ajax_download_filename', name='ajax_download_filename'),
            url(r'^filename-to-storename-json/$', 'manageApp.views.filename_to_storename_json', name="filename_to_storename_json"),
            url(r'^get-update-error-msg/$', 'manageApp.views.get_update_error_msg', name="get_update_error_msg"),
            url(r'^inventory-report-import/$', 'manageApp.views.inventory_import', name="inventory_import"),
            url(r'^inventory-report-upload/$', 'manageApp.views.inventory_import_upload', name="inventory_import_upload"),


            url(r'^other-handle-import/$', 'manageApp.views.other_handle_import', name="other_handle_import"),
            url(r'^other-handle-upload/$', 'manageApp.views.other_handle_upload', name="other_handle_upload"),
            url(r'^other-handle-upload-data/$', 'manageApp.views.other_handle_upload_data', name="other_handle_upload_data"),
            url(r'^other_handle_ajax_upload/$', 'manageApp.views.other_handle_ajax_upload', name="other_handle_ajax_upload"),
            url(r'^other-handle-file-delet/$', 'manageApp.views.other_handle_file_delet',name="other_handle_file_delet"),


                       )

urlpatterns += patterns('',
                        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.STATICFILES_DIRS[1],
                            }),
                        )



