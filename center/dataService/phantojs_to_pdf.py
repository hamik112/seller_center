# encoding:utf-8

import os

from django.conf import settings
from selenium import webdriver

base_dir = settings.BASE_DIR

phantomjs_path = os.path.join(base_dir, "center/dataService/phantomjs")

def execute(driver, script, args):
    driver.execute('executePhantomScript', {'script': script, 'args' : args })

def html_to_pdf(result_path_html , filename):
    driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    # hack while the python interface lags

    driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
    driver.get(result_path_html)   #
    #driver.get('http://localhost:8080/summary-pdf/')

    # set page format
    # inside the execution script, webpage is "this"
    pageFormat = '''this.paperSize = {format: "A4", orientation: "portrait" };'''
    execute(driver, pageFormat, [])

    # render current page
    render = '''this.render("'''+filename+'''")'''
    execute(driver, render, [])
    driver.quit()
    return filename


