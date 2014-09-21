__all__ = [ 'settings', 'HttpResponse', 'HttpResponseRedirect',
            'ApiBaseError', 'WebBaseError', 'Web404',
            'render_tpl', 'render_api',
            'only_method', 'get_rsrc', 'check_params', ]

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.conf import settings
from django.utils.http import urlquote
from django.core.context_processors import csrf

from utils.json import _dic, _json

class ApiBaseError(Exception):
    ERROR_CODES = {
        400: 'Bad Request',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        500: 'Internal Server Error'
    }

    def __init__(self, code, msg=None):
        if not code in self.ERROR_CODES:
            raise ValueError
        self.code = code
        self.msg = msg

    def __str__(self):
        return repr(self.code)

    @property
    def default_msg(self):
        return self.ERROR_CODES[self.code]

    def get_msg(self):
        if self.msg:
            return '%s: %s' % (self.default_msg,
                                self.msg)
        else:
            return self.default_msg

    def get_resp(self):
        data = dict(
                error = self.get_msg())

        resp = HttpResponse(_json(data),
                            status=self.code)
        return resp

class WebBaseError(Exception):
    pass

class Web404(WebBaseError):
    pass

def render_tpl(request, tpl, cdic={}):
    cdic['request'] = request
    cdic.update(csrf(request))
    return render_to_response(
        tpl,
        cdic
    )

def _render_tpl(tpl_name, cdic={}):
    tpl = get_template(tpl_name)
    context = Context(cdic)
    return tpl.render(context)

def render_api(data):
    json = _json(data)
    return HttpResponse(json, content_type='application/json')

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

class get_rsrc:
    def __init__(self, model, arg_name):
        from django.db.models import get_model
        if isinstance(model, str) or isinstance(model, unicode):
            self.model = get_model(*model.split('.'))
        else:
            self.model = model
        self.arg_name = arg_name

    def __call__(self, fn, *args, **kwargs):
        def _wrapper(req, *args, **kwargs):
            user = req.user

            if 'POST' == req.method:
                arg = req.POST.get(self.arg_name)
            else:
                arg = req.GET.get(self.arg_name)

            try:
                arg = int(arg)
            except:
                raise ApiBaseError(400)

            try:
                req._target = self.model.objects.get(pk=arg)
            except:
                raise ApiBaseError(404, self.model.__name__)

            return fn(req, *args, **kwargs)
        return _wrapper

class check_params:
    def __init__(self, params=[]):
        self.params = params

    def __call__(self, fn, *args, **kwargs):
        def _wrapper(req, *args, **kwargs):
            if 'POST' == req.method:
                origin = req.POST
            else:
                origin = req.GET

            for i in self.params:
                if i not in origin:
                    raise ApiBaseError(400, 'Params Not Complete')

            return fn(req, *args, **kwargs)
        return _wrapper
