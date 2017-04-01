#!/usr/bin/env python 
# encoding:utf-8


from center.tasks import data_range_reports_tasks
from center.dataService.statement_view_data import StatementViewData
from center.models import GenerateReport



def generate_data_range_reports(request):
    """使用tasks任务去生成pdf，因为量大，时间长"""
    #GenerateReport
    statusCode = "OK"
    username , post_dict = request.user.username, request.POST
    print "*"*100
    return_dict = {}
    try:
        return_dict = StatementViewData(username, post_dict, return_dict).write_recorde_generate_report(action_statue="1")
        # StatementViewData(username, post_dict, return_dict).request_report()
        data_range_reports_tasks.delay(username, post_dict, return_dict)
    except Exception, e:
        print "data_range report tasks Error: %s" % str(e)
        statusCode = ""
    return {"statusCode":statusCode}



def generate_reports_again(line_id, username):
    statusCode = "OK"
    try:
        post_dict = GenerateReport.objects.filter(id=line_id).values("is_custom","month", "reportType", "report_file_path", "request_date", "timeRange", "timeRangeType", "year")
        GenerateReport.objects.filter(id=line_id).update(action_statue="1")
        return_dict = {}
        data_range_reports_tasks.delay(username, post_dict, return_dict)
    except Exception, e:
        print "generate reports again Error: %s" % str(e)
        statusCode = ""
    return {"statusCode": statusCode}

