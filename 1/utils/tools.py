import os
import sys
import time
import urllib
import httplib
from hashlib import md5

from utils.upload import S3Upload

import config

class SDict(dict):
    """
    Copy from web.utils.Stroage
    Usage:
        >>> o = Storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
    """
    def __init__(self, dic=None):
        if dic:
            for k in dic.keys():
                self.__setattr__(k, dic[k])
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            #raise AttributeError, k
            return None
    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k
    def __repr__(self):
        return '<Storage> ' + dict.__repr__(self)
    def out(self):
        dic = {}
        for k in self.keys():
            dic[k] = self[k]
        return dic

def urlfetch(domain, url, secure=True):
    if secure:
        conn = httplib.HTTPSConnection(domain)
    else:
        conn = httplib.HTTPConnection(domain)
    conn.request('GET', url)
    resp = conn.getresponse()
    return resp.read()

def urlpost(domain, url,
        data={},
        headers={},
        secure=True):
    if secure:
        conn = httplib.HTTPSConnection(domain)
    else:
        conn = httplib.HTTPConnection(domain)
    data = urllib.urlencode(data)
    print 'urlpost data', data
    conn.request('POST', url, data, headers)
    resp = conn.getresponse()
    return resp.read()

def exstr(x):
    if isinstance(x, unicode):
        return x.encode('utf-8')
    return x

def sort_dictList(l):
    sortedList = []
    #tupList = []
    #numList = []

    for loop0, i in enumerate(l):
        print i['timestamp']
        if 0 == loop0:
            sortedList.append(i)
        else:
            for loop1, j in enumerate(sortedList):
                if i['timestamp'] > j['timestamp']:
                    sortedList.insert(loop1, i)
                else:
                    sortedList.append(i)
                break

    return sortedList

if '__main__' == __name__:
    email = 'reorx@gmail.com'
    generate_qr(email)
