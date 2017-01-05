# encoding:utf-8

import os
import sys
from gevent import monkey;
monkey.patch_all()
from gevent.wsgi import WSGIServer



# 将系统的编码设置为UTF8
reload(sys)
sys.setdefaultencoding('utf8')



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SellerCenter.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#host = "0.0.0.0"
#port = 8080
# server = WSGIServer((host, port), application)
# print ("Starting server on http://%s:%s"%(str(host), str(port)))
# server.serve_forever()



