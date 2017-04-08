#encoding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import  settings

urlpatterns = patterns('',
            url(r'^$', 'center.views.home', name='home'),
            url(r'^home/$', 'center.views.home', name="home"),

            url(r'transaction/$', 'center.views.transaction', name='payment'),
            url(r'transaction/transaction-data/$', 'center.views.transaction_data', name='transaction_data'),
            url(r'transaction/transaction-data-download/$', 'center.views.transaction_data_download', name='transaction_data_download'),


            url(r'inventory/$', 'center.views.inventory', name='inventory'),
            url(r'inventory/inventory-reports/$', 'center.views.inventory_reports', name='inventory_reports'),
            url(r'listing/reports/$', 'center.views.listing_reports', name="listing_reports"),
                       
            url(r'inventory/inventory-reports-data/$', 'center.views.inventory_reports_data', name='inventory_report_data'),
            url(r'inventory/inventory-FBA-shipping/$','center.views.inventory_FBA_shipping', name='inventory_FBA_shipping'),
            url(r'gp/fba/core/data/collections/shipments.html', 'center.views.inventory_FBA_shipping_shipments', name='inventory_FBA_shipping_shipments'),
            url(r'gp/fba/core/data/collections/manifests.html', 'center.views.inventory_FBA_shipping_manifests', name='inventory_FBA_shipping_manifests'),

            url(r'all-statements/$', 'center.views.all_statements', name='all_statements'),
            url(r'all-statements-download/$', 'center.views.download_all_statements', name='download_all_statements'),
            url(r'date-range-reports/$', 'center.views.date_range_reports', name='date_range_reports'),
            url(r'date-range-reports/request-report-again/$', 'center.views.request_report_again', name='request_report_again'),


            url(r'statement-view/$', 'center.views.statement_view', name='statement_view'),
            url(r'pricing/$', 'center.views.pricing', name='pricing'),
            url(r'orders/$', 'center.views.orders', name='orders'),
            url(r'advertising/$', 'center.views.advertising', name='advertising'),
            url(r'performance/$', 'center.views.performance', name='performance'),


            url(r'summary-pdf/$', 'center.views.pdf_file_view', name='pdf_file_view'),

            url(r'download-file/$', 'center.views.download_file', name='download_file'),

            url(r'amazon-login/$', 'center.views.amazon_login', name='amazon_login'),
            url(r'amazon-register/$', 'center.views.amazon_register', name='amazon_register'),
            url(r'amazon-logout/$', 'center.views.amazon_logout', name='amazon_logout'),
                      )


urlpatterns += patterns('',
                        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.STATICFILES_DIRS[0],
                             }),
                        )

