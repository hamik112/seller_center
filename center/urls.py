#encoding:utf-8
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
            url(r'^$', 'center.views.home', name='home'),
            url(r'^home/$', 'center.views.home', name="home"),

            url(r'transaction/$', 'center.views.transaction', name='payment'),
            url(r'inventory/$', 'center.views.inventory', name='inventory'),
            url(r'all-statements/$', 'center.views.all_statements', name='all_statements'),
            url(r'date-range-reports/$', 'center.views.date_range_reports', name='date_range_reports'),
            url(r'statement-view/$', 'center.views.statement_view', name='statement_view'),
            url(r'pricing/$', 'center.views.pricing', name='pricing'),
            url(r'orders/$', 'center.views.orders', name='orders'),
            url(r'advertising/$', 'center.views.advertising', name='advertising'),
            url(r'performance/$', 'center.views.performance', name='performance'),

            url(r'summary-pdf/$', 'center.views.pdf_file_view', name='pdf_file_view'),
                      )
