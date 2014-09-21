#encoding:utf-8
# Create your views here.


# from pymmseg import mmseg
from django.http import HttpResponse
from models import Index, IndexFictionRelationship, SearchRecord, SearchKeyWord
from django.template import RequestContext
from django.utils.http import urlquote
from django.shortcuts import render_to_response as RTR
import threading
# use memcache
# from django.core.cache import cache
from crawler.crawler_config import WEB_SITE
# mmseg.dict_load_defaults()


def POST_ONLY(method):
    def wrapper(request, *args):
        if request.method == 'GET':
            return HttpResponse('method not allowed!')
        return method(request)
    return wrapper

def save_search_record(q, ip, item, user, out_n):
    """save search record"""
    try:
        key_word = SearchKeyWord.objects.get(words = item)
    except:
        key_word = SearchKeyWord(words = item)
        key_word.save()
    key_word.record_time += 1
    key_word.out_number += out_n
    key_word.save()
    search_record = SearchRecord(key_word = key_word,
        ip = ip,
        total_word = q,
        recorder = user.nid if user.is_authenticated() else '0')
    search_record.save()


def get_html_content(title, posi):
    new_content = ""
    last = 0
    if isinstance(title, unicode):
        title = title.encode('utf-8')
    hashs = {}
    out_past = []
    for item in posi:
        out_past.append([int(item[0]), int(item[1])])
    out_past.sort(lambda x,y : cmp(x[0], y[0]))
    for item in out_past:
        if hashs.has_key(str(item[0])):
            continue
        hashs[str(item[0])] = 1
        contents = title[last: int(item[0])]
        new_content += "<font color=black>" + contents + "</font>"
        tag = True
        for bit in range(int(item[0]), int(item[1])):
            if ord(title[bit]) >= 0x4e00 and ord(title[bit]) < 0x9fa6:
                tag = False
        if tag:
            new_content += "<font color=red>" + title[int(item[0]): int(item[1])] + "</font>"
        else:
            new_content += "<font color=red>" + title[int(item[0]) / 3: int(item[1]) / 3] + "</font>"
        last = int(item[1])
    tag = True
    for bit in range(int(item[1]), len(title)):
        if ord(title[bit]) >= 0x4e00 and ord(title[bit]) < 0x9fa6:
            tag = False
    if tag:
        new_content += "<font color=black>" + title[int(item[1]): len(title)] + "</font>"
    else:
        new_content += "<font color=black>" + title[int(item[1]) / 3: len(title) / 3] + "</font>"
    return new_content 

def search_engine(request, key_word, types, page_nid = 0):
    
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    outcome, fictions = {}, {}
    score, category = {}, {}
    category = {"c1" : 0, "c22" : 0, "c3" : 0, "c5" : 0, "c6" : 0, "c7" : 0, "c8" : 0, "c9" : 0, "c10" : 0, "c12" : 0, "c14" : 0, "c31" : 0, "c41" : 0, 'c4' : 0, 'c21' : 0, 'c15' : 0, "c2" : 0}
    posi, first_page = {}, []
    #clean session
    for item in category.keys():
        if item[1:] in request.session:
            del request.session[item[1:]]
    #get search outcome
    Lock = {}
    seg_ret = [item.text for item in mmseg.Algorithm(key_word)]
    seg_ret = list(set(seg_ret))
    for item in seg_ret:
        if len(item) < 6:
            continue
        try:
            collection = Index.objects.get(key = item)
        except:
            collection = None
        #获取所有的小说
        if types == '0':#如果是全部
            try:
                collections = collection.fiction.all()
                number = len(collections)
            except:
                number = 0
        else:#某一个类别
            try:
                collections = collection.fiction.filter(fiction_style = types)
                number = len(collections)
            except Exception, e:
                print e
                number = 0
        try:
            t = threading.Thread(target = save_search_record, args = (key_word, ip, item, request.user, number))
            t.start()
            t.join()
        except Exception, e:
            print e
        if number == 0:
            continue
        for items in collections:
            id_key = str(items.id)
            fiction_indexes = IndexFictionRelationship.objects.filter(fiction = items, key = collection)
            temp = []
            for pos in fiction_indexes: 
                pos_str = pos.position.split(',')
                if not posi.has_key(id_key):
                    posi[id_key] = []
                posi[id_key].append(pos_str)
                temp.append(pos_str)
                if score.has_key(id_key) == False:
                    score[id_key] = 0
                score[id_key] += 1.0 / int(pos.bit) if pos.bit == '1' else 1.0 / (10 * int(pos.bit))
            fictions[id_key] = items
            #save session
            """
            ATTENTION
            MEMCACHE REPLACED
            """
    #sort score
    score = sorted(score.items(), lambda x,y : -cmp(x[1], y[1]))
    score = score[:200]
    #total page_number
    total_page_number = (len(score) - 1) / 10 + 1
    styles = {"1" : "奇幻", "22" : "武侠", "3" : "仙侠", "5" : "历史", "6" : "军事", 
        "7" : "游戏", "8" : "竞技", "9" : "科幻", "10" : "灵异", "12" : "同人", "2" : "武侠",
        "14" : "图文", "31" : "文学", "41" : "女生", '4' : '都市', '21' : '玄幻', '15' : '青春'}
    website = WEB_SITE
    #clean the memcache
    #save the 2nd-5th page to memcache
    #for item in range(2, total_page_number):
    #    cache.set(str(ip) + str(item), 'sdf')
    #get the first page's content
    style_cnt = {"0" : 0,"1" : 0, "22" : 0, "3" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0, "10" : 0, "12" : 0, "14" : 0, "31" : 0, "41" : 0, '4' : 0, '21' : 0, '15' : 0, "2" : 0}
    
    #clean session
    if types == '0' and page_nid == 0:
        for item in range(1,5):
            for t in style_cnt.keys():
                try:
                    del request.session[t + '_' + str(item)]
                except:
                    pass
    stp = 0
    if page_nid > 2:
        score = score[10 * page_nid - 10 : 10 * page_nid]
    for ids, scores in score:
        if not Lock.has_key(ids):
            category['c' + fictions[ids].fiction_style] += 1
            Lock[ids] = 1
            #get positioin and score

        #get the category
        style = styles[fictions[ids].fiction_style]
        if isinstance(style, unicode):
            style = style.encode('utf-8')
        stp += 1
        if stp <= 10:
            new_intro = get_html_content(fictions[ids].fiction_title, posi[ids])
            first_page.append({'fiction_title' : new_intro,
                'fiction_url' : fictions[ids].fiction_avatar_url,
                'posi' : str(((posi[ids]))),
                'fiction_author' : fictions[ids].author,
                'fiction_author_url' : fictions[ids].author_url,
                'fiction_website' : '..',
                'fiction_score' : '暂无评分' if fictions[ids].grading_number == 0 else fictions[ids].grading_total * 1.0 \
                    / fictions[ids].grading_number,
                'fiction_id' : fictions[ids].id,
                'fiction_nid' : fictions[ids].fiction_nid,
                'fiction_style' : style,
                'fiction_site' : website[fictions[ids].source_site.title]['name'],
                'fiction_intro' : fictions[ids].fiction_intro[:90],
                'fiction_total' : fictions[ids].total_word,
                'fiction_com' : fictions[ids].com_word,
                'click_time' : fictions[ids].click_time,
                'rec_time' : fictions[ids].rec_time,
                })
        
        if types == '0' and page_nid < 3:
            typ = fictions[ids].fiction_style 
            cnt = style_cnt[typ]
            cnt_all = style_cnt['0']
            page_number = int((cnt) / 10) + 1
            page_number_all = int((cnt_all) / 10) + 1
            if page_number < 3:
                style_cnt[typ] += 1
                session_key = str(typ) + '_' + str(page_number)
                if session_key not in request.session:
                    request.session[session_key] = []
                request.session[session_key].append({\
                    'fiction' : fictions[ids],
                    'position' : posi[ids]})
            if page_number_all < 3:
                style_cnt['0'] += 1
                session_key_all = '0_' + str(page_number_all)
                if session_key_all not in request.session:
                    request.session[session_key_all] = []
                request.session[session_key_all].append({\
                    'fiction' : fictions[ids],
                    'position' : posi[ids]})
        #save the continus 4 page into memcache
    if types == '0' and page_nid == 0:
        return first_page, len(score), category, total_page_number
    else:
        return first_page

def search(request):
    """search method for url /search?q=&type="""
    if request.method == 'GET':
        #get pageindex
        page_index = request.GET.get('page_index', '')
        if page_index:
            out = cache.get(str(ip))
            return HttpResponse(out[str(page_index)])
        else:
            q = request.GET.get('q', '')
            types = request.GET.get('types', '')
    else:
        q = request.POST.get('q', '')
        types = request.POST.get('type', '') 
    if not types:
        types = '0'
    if isinstance(q, unicode):
        q = q.encode('utf-8')

    first_page, tot_search_outcome, category, total_page_number = search_engine(request, q, types)
    #save search record
    cdic = {'outcome' : first_page, 
        'key_word' : str(q), 
        'is_auth' : request.user.is_authenticated(),
        'user' : request.user,
        'total_page' : total_page_number,
        'category' : category,
        'total' : tot_search_outcome}
    return RTR('result.html', cdic, context_instance = RequestContext(request))

@POST_ONLY
def search_detail_style(request): 
    import string 
    style = request.POST.get('style', '')
    page_nid = request.POST.get('page_nid', '')
    print 'yes'
    q = request.POST.get('q', '')
    if isinstance(q, unicode):
        q = q.encode('utf-8')
    print q, type(q)
    if not style or not page_nid:
        return HttpResponse('error')
    else:
        ret = []
        website = WEB_SITE
        styles = {"1" : "奇幻", "22" : "武侠", "3" : "仙侠", "5" : "历史", "6" : "军事", 
            "7" : "游戏", "8" : "竞技", "9" : "科幻", "10" : "灵异", "12" : "同人", "2" : "武侠",
            "14" : "图文", "31" : "文学", "41" : "女生", '4' : '都市', '21' : '玄幻', '15' : '青春'}
        #if search page is smaller than 2, just request for the session
        if int(page_nid) <= 2:
            for item in request.session[style + '_' + page_nid]: 
                fiction = item['fiction']
                posi = item['position']
                new_intro = get_html_content(fiction.fiction_title, posi) 
                new_intro = string.replace(new_intro, '>', '-')
                new_intro = string.replace(new_intro, '<', '+')
                ret.append({'fiction_url' : fiction.fiction_avatar_url,
                    'fiction_title' : string.replace(new_intro, '=', '*'),
                    'fiction_score' : '暂无评分' if fiction.grading_number == 0 else fiction.grading_total * 1.0 \
                        / fiction.grading_number,
                    'fiction_id' : fiction.id,
                    'fiction_nid' : fiction.fiction_nid,
                    'fiction_style' : styles[fiction.fiction_style],
                    'fiction_site' : website[fiction.source_site.title]['name'],
                    'fiction_author' : fiction.author,
                    'fiction_intro' : fiction.fiction_intro[:90]})
            try:
                import simplejson as json
            except:
                import json
            return HttpResponse(json.dumps(ret))
        else:
            print '..',q
            if isinstance(q, unicode):
                q = q.encode('utf-8')
            first_page = search_engine(request, q, style, int(page_nid))
            for item in first_page:
                item['fiction_title'] = string.replace(item['fiction_title'], '>', '-')
                item['fiction_title'] = string.replace(item['fiction_title'], '<', '+')
            try:
                import simplejson as json
            except:
                import json
            print first_page
            return HttpResponse(json.dumps(first_page))
    return HttpResponse("no")
