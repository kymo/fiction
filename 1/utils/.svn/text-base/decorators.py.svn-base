from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlquote
from django.conf import settings
from django.utils.importlib import import_module

from utils.json import _dic, _json
from utils.viewbase import render_api
from utils.errors import ApiBaseError

class only_method:
    def __init__(self, method):
        self.method = method
    def __call__(self, fn, *args, **kwargs):
        def _wrapper(req, *args, **kwargs):
            if self.method == req.method:
                return fn(req, *args, **kwargs)
            resp= HttpResponse('Method Not Allowed', status=405)
            return resp
        return _wrapper

def login_required(fn):
    def _wrapper(req, *args, **kwargs):
        if not req.user.is_authenticated:
            print 'User Not Authed'
            if req.is_server:
                raise ApiBaseError(400, 'Need Login')
            else:
                return HttpResponseRedirect( '%s?to=%s' %
                        (settings.LOGIN_URL, urlquote(req.get_full_path())) )
        return fn(req, *args, **kwargs)
    return _wrapper

class post_resolve:
    """
    for POST
    """
    # TODO receive fields, check for debug
    def __init__(self, field_list=[]):
        self.field_list = field_list
    def __call__(self, fn, *args, **kwargs):
        def _wrapper(req, *args, **kwargs):
            #if req.is_server:
            print 'post_resolve'
            if 'POST' == req.method:
                json = req.POST.get('json')
                if not json:
                    raise ApiBaseError(400, 'Post Data Passing Error')
                #print 'RAW JSON            : [%s] %s' % (type(json), json[:100])
                print 'RAW JSON            : [%s] %s' % (type(json), json[:500])

                try:
                    postData = _dic(json)
                except:
                    raise ApiBaseError(400, 'Post Data Format Error')
                #print 'POST DATA           : [%s] %s' % (type(postData), postData)

                # field check
                for i in self.field_list:
                    if not i in postData:
                        raise ApiBaseError(400, 'Post Data Params Error')

                req._post_data = postData

            if 'GET' == req.method:
                raise ApiBaseError(400, 'Method GET Not Allowed')
            return fn(req, *args, **kwargs)
        return _wrapper

def with_mobile_only(fn):
    def _wrapper(req, *args, **kwargs):
        from mobile.models import Mobile
        if not isinstance(req.user.mobile, Mobile):
            raise ApiBaseError(400, 'Only Socket Server \
                    with Proper IMEI Allowed')
        return fn(req, *args, **kwargs)
    return _wrapper
