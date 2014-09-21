#coding=utf-8
#try:
    #import cjson as pyjson # cjson is more effective
    # cjson is suck with Chinese character
#except ImportError:
    #from django.utils import simplejson as pyjson
import datetime
from django.utils import simplejson as pyjson

class DateTimeJSONEncoder(pyjson.JSONEncoder):
    """
    copy from django.core.serializers.json
    """
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
        elif isinstance(o, datetime.date):
            return o.strftime(self.DATE_FORMAT)
        elif isinstance(o, datetime.time):
            return o.strftime(self.TIME_FORMAT)
        else:
            return super(DateTimeJSONEncoder, self).default(o)

def _dic(json):
    return pyjson.loads(json, encoding='utf-8')

def _json(dic):
    return pyjson.dumps(dic, ensure_ascii=False, cls=DateTimeJSONEncoder)

