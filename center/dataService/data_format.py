# encoding:utf-8

import  os
from django.conf import settings

GENERATOR_PATH = settings.GENERATE_REPORT_PATH



def file_iterator(file_name, chunk_size=512):
    file_name_path = os.path.join(GENERATOR_PATH, file_name)
    with open(file_name_path) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
