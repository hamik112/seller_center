# encoding:utf-8

import  os
from django.conf import settings

GENERATOR_PATH = settings.GENERATE_REPORT_PATH
ALL_STATEMENTS_FILE_PATH =  settings.ALL_STATEMENTS_FILE_PATH


def file_iterator(file_name, chunk_size=512):
    print "file_name",file_name
    file_name_path = os.path.join(GENERATOR_PATH, file_name)
    with open(file_name_path) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def file_iterator_all_statement(file_name, chunk_size=512):
    file_name_path = os.path.join(ALL_STATEMENTS_FILE_PATH, file_name)
    print "file_name_path:", file_name_path
    with open(file_name_path) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break



