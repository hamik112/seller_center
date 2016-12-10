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



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bw(d18y*zpt!r()bsu45c_=_o%+pi398=mtq89v0s65j)=xo1j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



#djcelery+broker配置
import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://127.0.0.1:6379/0'
#或者
#BROKER_HOST = "192.168.1.83"
#BROKER_PORT = 6379
#BROKER_USER = ""
#BROKER_PASSWORD = ""
#BROKER_VHOST = "0"




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
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# LANGUAGE_CODE = 'zh-CN'
# TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'



UPLOAD_PATH = os.path.join(BASE_DIR, "manageApp/UploadFilePath")                #上传文件路径
if not os.path.exists(UPLOAD_PATH):
    os.mkdir(UPLOAD_PATH)


GENERATE_REPORT_PATH = os.path.join(BASE_DIR, "center/GENERATE_REPORT")  #生成的报表路径
if not os.path.exists(GENERATE_REPORT_PATH):
    os.mkdir(GENERATE_REPORT_PATH)

