# -*- coding:UTF-8 -*-
import json
from datetime import datetime, date
from decimal import *

import pytz
import types
from django.conf import settings
from django.db import models
from django.db.models.base import ModelState


def json_encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to a object dynamically are being ignored (and it also has
    problems with some models).
    """

    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        elif isinstance(data, ModelState):
            ret = None
        elif isinstance(data, datetime):
            ret = data.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.CN_TIME_ZONE)).strftime(
                '%Y-%m-%d %H:%M:%S')
        elif isinstance(data, date):
            ret = data.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.CN_TIME_ZONE)).strftime('%Y-%m-%d')
            # elif isinstance(data, django.db.models.fields.related.RelatedManager):
            #    ret = _list(data.all())
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k, v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)
    return json.dumps(ret)
