#encoding:utf-8
# Create your views here.

from django.http import HttpResponse
from search.views import POST_ONLY
from django.template import RequestContext
from django.shortcuts import render_to_response as RTR
from models import Advice
def index_iknow(request):
    ret = {'user' : request.user,
        'is_auth' : request.user.is_authenticated()}
    return RTR('iknow.html', ret, context_instance = RequestContext(request))

@POST_ONLY
def get_advice(request):
    
    advice = request.POST.get('advice', '')
    frm = request.POST.get('frm', '')
    ad = Advice(advice = advice,
        frm = frm)
    ad.save()

    return HttpResponse('ok')
