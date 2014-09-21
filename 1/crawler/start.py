#encoding:utf-8


import urllib2

req = urllib2.urlopen("http://127.0.0.1:8000/xs7/spider_start/")

print req.read()


