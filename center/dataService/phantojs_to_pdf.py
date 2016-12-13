

# encoding:utf-8

from selenium import webdriver

def execute(driver, script, args):
    driver.execute('executePhantomScript', {'script': script, 'args' : args })

def html_to_pdf(filename):
    driver = webdriver.PhantomJS('phantomjs')
    # hack while the python interface lags

    driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')

    driver.get('http://localhost:8080/summary-pdf/')

    # set page format
    # inside the execution script, webpage is "this"
    pageFormat = '''this.paperSize = {format: "A4", orientation: "portrait" };'''
    execute(driver, pageFormat, [])

    # render current page
    render = '''this.render("'''+filename+'''")'''
    execute(driver, render, [])
