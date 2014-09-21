# Create your views here.

from spider_thread import xs8_test, book630_test, longtengzw_test
from django.http import HttpResponse
from crawler import qidian_crawler, book630_crawler, aoye_crawler, test_crawler
from django.shortcuts import render_to_response as RTR

def spider_start(request):
    xs8_test()
    longtengzw_test()
    #print 'yes'
    book630_test()
    #book630_crawler()
    return HttpResponse('yes')
def update_thread(request):
    #qidian_crawler()
    #aoye_crawler()
    book630_crawler()
    #url = "/Book/2494758.aspx"
    #url = "/Book/2418504.aspx"
    #test_crawler(url)
    return HttpResponse('yes')
