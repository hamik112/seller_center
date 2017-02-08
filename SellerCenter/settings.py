# encoding:utf-8
"""
Django settings for SellerCenter project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import getpass


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bw(d18y*zpt!r()bsu45c_=_o%+pi398=mtq89v0s65j)=xo1j'

# SECURITY WARNING: don't run with debug turned on in production!
cur_user = getpass.getuser()
if cur_user == "seller_center":
    DEBUG = False
    ALLOWED_HOSTS = ["47.89.49.243"]
else:
    DEBUG = True
    ALLOWED_HOSTS = []



#djcelery+broker配置
from kombu import Queue, Exchange
import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://127.0.0.1:6379/0'
#或者
#BROKER_HOST = "192.168.1.83"
#BROKER_PORT = 6379
#BROKER_USER = ""
#BROKER_PASSWORD = ""
#BROKER_VHOST = "0"

CELERYD_MAX_TASKS_PER_CHILD = 40 # 每个worker执行了多少任务就会死掉

CELERY_QUEUES = (
    #"default_task": {
    #    "queue": "default"
    #},
    #"download_task":{
    #    "queue": "download"
    #}
    Queue("celery", routing_key="celery"),
    Queue('download',
          exchange=Exchange('download', type='direct'),
          routing_key='download_key'),
)

CELERY_ROUTES = {
    "center.tasks.get_amazon_report": {
        "queue": "download",
        "routing_key": "download_key",
    },
    "center.tasks.download_import_report_task":{
        "queue": "download",
        "routing_key": "download_key",
    },
    "center.tasks.data_range_reports_tasks": {
        "queue": "download",
        "routing_key": "download_key",
    }
}




# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'center',
    'manageApp',
    'djcelery',
    #'kombu.transport.django'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'SellerCenter.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "manageApp/templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SellerCenter.wsgi.application'






# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "seller_center",
        "USER": "root",
        "PASSWORD": "admin",
        "HOST": "",
        "PORT": ""
    }
}
        

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'zh-CN'
TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "center/static/"),
    os.path.join(BASE_DIR, "manageApp/static/"),
)

#print STATICFILES_DIRS


UPLOAD_PATH = os.path.join(BASE_DIR, "manageApp/UploadFilePath")                #上传文件路径
if not os.path.exists(UPLOAD_PATH):
    os.mkdir(UPLOAD_PATH)


GENERATE_REPORT_PATH = os.path.join(BASE_DIR, "center/GENERATE_REPORT")  #生成的报表路径
if not os.path.exists(GENERATE_REPORT_PATH):
    os.mkdir(GENERATE_REPORT_PATH)


ALL_STATEMENTS_FILE_PATH = os.path.join(BASE_DIR, "center/ALL_STATEMENTS_FILES")
if not os.path.exists(ALL_STATEMENTS_FILE_PATH):
    os.mkdir(ALL_STATEMENTS_FILE_PATH)



app_path = os.path.join(BASE_DIR, "center")


LOG_PATH = os.path.join(app_path, "log")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


# LOGGING = {
#         'version': 1,
#         'disable_existing_loggers': True,
#         'formatters': {
#         'standard': {
#         'format': '%(levelname)s %(asctime)s %(message)s'
#         },
#     },
#     'filters': {
#     },
#     'handlers': {
#         'mail_admins': {
#                         'level': 'ERROR',
#                         'class': 'django.utils.log.AdminEmailHandler',
#                         'formatter':'standard',
#         },
#         'test1_handler': {
#                         'level':'DEBUG',
#                         'class':'logging.handlers.RotatingFileHandler',
#                         'filename':os.path.join(LOG_PATH, "access.log"),
#                         'formatter':'standard',
#         },
#         'test2_handler': {
#                         'level':'DEBUG',
#                         'class':'logging.handlers.RotatingFileHandler',
#                         'filename':os.path.join(LOG_PATH,"get_post_data.log"),
#                         'formatter':'standard',
#         },
#     },
#     'loggers': {
#         'django.request': {
#                         'handlers': ['mail_admins'],
#                         'level': 'ERROR',
#                         'propagate': True,
#         },
#         'test1':{
#                         'handlers': ['test1_handler'],
#                         'level': 'INFO',
#                         'propagate': False
#         },
#         'test2':{
#                 'handlers': ['test2_handler'],
#                 'level': 'INFO',
#                 'propagate': False
#         },
#     }
# }
#


#导入模块
import logging
import django.utils.log
import logging.handlers

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
       'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}  #日志格式
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, "default.log"),     #日志输出文件
            'maxBytes': 1024*1024*5,                  #文件大小
            'backupCount': 5,                         #备份份数
            'formatter':'standard',                   #使用哪种formatters日志格式
        },
        'error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, "error.log"),
            'maxBytes':1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, "request_handler.log"),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join(LOG_PATH, "scripts.log"),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'tasks_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, "tasks.log"),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'tasks': {
            'handlers': ['tasks_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'file_out.views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'error':{
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}
