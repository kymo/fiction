# Create your views here.
#encoding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response as RTR
from django.template import RequestContext
from fiction.models import Fiction, ChapterIndex, Chapter, ChapterUrl
from shelf.models import ShelfFictionRelationship
from reader.models import Score
from django.utils.http import urlquote
from search.views import POST_ONLY
from crawler.crawler_config import WEB_SITE

@POST_ONLY
def grading(request):
    score = request.POST.get('score', '')
    fiction_nid = request.POST.get('fiction_nid' ,'')
    try:
        fiction = Fiction.objects.get(fiction_nid = fiction_nid)
        fiction.grading_number += 1
        fiction.grading_total += int(score)
        fiction.save()
    except:
        return HttpResponse('no')
    if request.user.is_authenticated():
        User = request.user
    else:
        return HttpResponse('no')
    score = Score(score = int(score), 
        fiction = fiction,
        recoreder = User)
    score.save()
    return HttpResponse('ok')

def board(request): 
    return RTR('board.html', {})

def all_chapters(request, nid, pid): 
    #get fiction by nid
    try:
        fiction = Fiction.objects.get(fiction_nid = nid)
    except:
        return HttpResponseRedirect('/error/')
    all_cnt = fiction.all_chapters.count()
    #print all_cnt
    if not pid:
        pid = 1
    tot_page_num = (all_cnt - 1) / 19 + 1
    pid = int(pid)
    if pid < 1:
        pid = 1
    if pid > tot_page_num:
        pid = tot_page_num
    #get all chapters
    chapters = fiction.all_chapters.all().order_by('index')[(pid - 1) * 19: pid * 19]
    try:
        fiction.update_time = str(chapters[0].record_time)[:19]
    except:
        fiction.update_time = "2010-12-15 23:25:23"
    for item in chapters:
        item.urls = item.all_urls.all()
        for url in item.urls:
            url.record_time = str(url.record_time)[:19]
            url.name = WEB_SITE[url.name]['name']
        idx = str(item.index)
        for items in range(4 - len(idx)):
            idx = '0' + idx
        item.idx = idx
    bef_cur_page, nxt_cur_page = [], []
    idx = 0
    for item in range(pid - 2, pid):
        if item >= 1:
            idx += 1
            bef_cur_page.append(item)
    for item in range(pid + 1, pid + 8 - idx):
        if item <= tot_page_num:
            nxt_cur_page.append(item)
    ret_dict = {
        'chapters' : chapters,
        'fiction' : fiction,
        'tot_num' : tot_page_num,
        'bef_cur_page' : bef_cur_page,
        'nxt_cur_page' : nxt_cur_page,
        'bef_page' : pid - 1,
        'nxt_page' : pid + 1,
        'pid' : pid,
        'r_page' : tot_page_num,
        }
    return RTR('catelog.html', ret_dict)
def chapter_home(request, nid, index):
    #get fiction by nid
    try:
        fiction = Fiction.objects.get(fiction_nid = nid)
    except:
        return HttpResponseRedirect('/error/')
    #get the chapter
    try:
        chapter_index = ChapterIndex.objects.filter(fiction = fiction.id)
    except Exception,e:
        return HttpResponseRedirect('/server_error/')
    newest_index = 1
    for item in chapter_index:
        newest_index = max(item.newest_index, newest_index)
    index = int(index)
    try:
        chapter = fiction.all_chapters.get(index = index)
    except:
        chapter = fiction.all_chapters.get(index = index - 1)
        index -= 1
    bef_chapter_index, next_chapter_index = index, index
    if index > 1:
        bef_chapter_index = index - 1
    if index < newest_index:
        next_chapter_index = index + 1

    #get the website which contains the chapter
    style = {'1' : '奇幻', '2' : '武侠', '22' : '仙侠', '4' : '都市', '5' : '历史', '6' : '军事', '7' : '游戏', '8' : '竞技',
        '9' : '科幻', '10' : '灵异', '12' : '同人', '14' : '图文', '31' : '文学', '41' : '女生', '21' : '玄幻', '15' :  '青春'} 
    fiction.style = style[fiction.fiction_style]
    fiction.score = '暂无评分' if fiction.grading_number == 0 else 1.0 * fiction.grading_total / fiction.grading_number
    chapter_urls = chapter.all_urls.all()
    idx = 1
    for item in chapter_urls:
        item.idx = idx
        item.record_time = str(item.record_time)
        item.name = WEB_SITE[item.name]['name']
        idx += 1
    ret_dict = {
        'fiction' : fiction,
        'fiction_site' : WEB_SITE[fiction.source_site.title]['name'],
        'chapter' : chapter,
        'index' : index,
        'chapter_urls' : chapter_urls,
        'next_chapter_index' : next_chapter_index,
        'bef_chapter_index' : bef_chapter_index
        }
    return RTR("chapter.html", ret_dict)

def fiction_home(request, nid):
    #get fiction by nid
    try:
        fiction = Fiction.objects.get(fiction_nid = nid)
    except:
        return HttpResponseRedirect('/error/')
    #get all chapters of this fiction
    chapters = fiction.all_chapters.all()[:10]
    asc_chapters = fiction.all_chapters.all().order_by('index')[:10]
    chapt_num = len(chapters)
    asc_chapter_num = len(asc_chapters)
    new_chapters = []
    new_asc_chapters = []
    for item in range(0, chapt_num, 2):
        new_chapters.append((chapters[item], chapters[item + 1]))
    for item in range(0, asc_chapter_num, 2):
        new_asc_chapters.append((asc_chapters[item], asc_chapters[item + 1]))
    is_auth = request.user.is_authenticated()
    #get the save kind fiction list
    if True:
        related_fiction = Fiction.objects.filter(fiction_style = fiction.fiction_style).order_by('-click_time', '-rec_time')[:12]
    else:
        related_fiction = None
    out,st = [], 1
    for item in related_fiction:
        if item != fiction:
            item.rank,st = st, st + 1
            out.append(item)
    for item in chapters:
        item.source.title = WEB_SITE[item.source.title]['name']
        item.record_time = str(item.record_time)[:19]
    
    style = {'1' : '奇幻', '2' : '武侠', '22' : '仙侠', '4' : '都市', '5' : '历史', '6' : '军事', '7' : '游戏', '8' : '竞技',
        '9' : '科幻', '10' : '灵异', '12' : '同人', '14' : '图文', '31' : '文学', '41' : '女生', '21' : '玄幻', '15' :  '青春'} 
    try:
        owned = ShelfFictionRelationship.objects.get(shelf = request.user.shelf,
            fiction = fiction)
        owned = True
    except:
        owned = False
    fiction.style = style[fiction.fiction_style]
    fiction.score = '暂无评分' if fiction.grading_number == 0 else 1.0 * fiction.grading_total / fiction.grading_number
    
    from_top = -6
    for item in out[1:]:
        item.top = from_top
        from_top -= 28
    
    #get newest update
    from_top = -6
    fictions_update_newest = Fiction.objects.all()[:11]
    update_out = [item for item in fictions_update_newest]
    for item in update_out[1:]:
        item.top = from_top
        from_top -= 28
    ret_dict = {'user' : request.user,
        'fiction' : fiction,
        'fiction_site' : WEB_SITE[fiction.source_site.title]['name'],
        'is_auth' : request.user.is_authenticated(),
        'chapters' : new_chapters,
        'asc_chapters' : new_asc_chapters,
        'related_fiction_rest' : out[1:],
        'first_one' : out[:1],
        'newest_fiction_one' : update_out[:1],
        'newest_fiction_rest' : update_out[1:],
        'chap_num' : chapt_num,
        'owned' : owned}
    return RTR('fiction.html', ret_dict, context_instance = RequestContext(request))


@POST_ONLY
def add_click_time_fiction(request):
    nid = request.POST.get('nid', '')
    try:
        fiction = Fiction.objects.get(fiction_nid = nid)
        fiction.click_time += 1
        fiction.save()
    except:
        return HttpResponse('no')
    return HttpResponse('ok')
@POST_ONLY
def add_click_time_chapter(request):
    nid = request.POST.get('nid', '')
    try:
        chapter = Chapter.objects.get(id = nid)
        chapter.click_time += 1
        chapter.save()
    except:
        return HttpResponse('no')
    return HttpResponse('ok')

@POST_ONLY
def load_fiction_from_type(request):
    types = request.POST.get('type', '')
    try:
        user_shelf = ShelfFictionRelationship.objects.filter(shelf = request.user.shelf)
    except:
        user_shelf = []
    out = []
    if types == '0':
        #get all
        for item in user_shelf:
            out.append({'avatar' : item.fiction.fiction_avatar_url,
                'nid' : item.fiction.fiction_nid,
                'title' : item.fiction.fiction_title[:6],
                'author' : item.fiction.author,
                'id' : item.id})
        try:
            import simplejson as json
        except:
            import json
        ret = json.dumps(out[:40])
        return HttpResponse(ret)
    for item in user_shelf:
        if item.fiction.fiction_style == types:
            out.append({'avatar' : item.fiction.fiction_avatar_url,
                'nid' : item.fiction.fiction_nid,
                'title' : item.fiction.fiction_title[:6],
                'author' : item.fiction.author,
                'id' : item.id})
    try:
        import simplejson as json
    except:
        import json
    return HttpResponse(json.dumps(out))

def read_book(request):
    chapter_id = request.GET.get('id','')
    book_url = request.GET.get('book_url' ,'')
    name = request.GET.get('frm', '')
    print chapter_id ,type(chapter_id)
    name = urlquote(name)
    print name
    try:
        chapter = Chapter.objects.get(id = int(chapter_id))
    except:
        try:
            chapter = NewestChapter.objects.get(id = int(chapter_id))
            chapter.index = ChapterIndex.objects.get(fiction = chapter.fiction.id, web_site = name)
        except:
            return HttpResponseRedirect('/error/')
    if chapter_id == '' or book_url == '' or name == '':
        return HttpResponseRedirect('/error/')
    try:
        bef = ChapterUrl.objects.get(fiction = chapter.fiction, index = chapter.index - 1, name = name)
    except:
        bef = None
    try:
        nxt = ChapterUrl.objects.get(fiction = chapter.fiction, index = chapter.index + 1, name = name)
    except:
        nxt = None
    nxt_title = nxt.chapter.chapter_title if nxt else '无'
    bef_title = bef.chapter.chapter_title if bef else '无'
    nxt_url = nxt.url if nxt else ''
    bef_url = bef.url if bef else ''
    all_urls = []
    nxt_id = nxt.chapter.id if nxt else ''
    bef_id = bef.chapter.id if bef else ''
    for item in chapter.all_urls.all():
        all_urls.append({'name' : WEB_SITE[item.name]['name'],
            'url' : item.url,
            'frm' : item.name})
    ret = {'cur_url' : book_url,
        'nxt_url' : nxt_url,
        'cur_id' : chapter_id,
        'bef_url' : bef_url,
        'all_urls' : all_urls,
        'nxt_id' : nxt_id,
        'bef_id' : bef_id,
        'frm' : name,
        'bef_title' : bef_title,
        'nxt_title' : nxt_title,
        'cur_title' : chapter.chapter_title,
        'fiction_nid' : chapter.fiction.fiction_nid,
        'fiction' : chapter.fiction.fiction_title}
    print ret
    return RTR('read_book.html', ret, context_instance = RequestContext(request))

@POST_ONLY
def get_recommond(request): 
    fictions = Fiction.objects.all().order_by('-click_time')[:5]
    ret = []
    for item in fictions:
        ret.append({'avatar' : item.fiction_avatar_url,
            'title' : item.fiction_title,
            'nid' : item.fiction_nid,
            'author' : item.author,
            'intro' : item.fiction_intro[:30]})
    try:
        import simplejson as json
    except:
        import json
    return HttpResponse(json.dumps(ret))

@POST_ONLY
def get_all_chapters(request):
    fiction_nid = request.POST.get('fiction_nid', '')
    try:
        fiction = Fiction.objects.get(fiction_nid = fiction_nid)
    except:
        return HttpResponse("服务器繁忙,请稍后再试..")
    all_chapters = fiction.all_chapters.all()
    ret_an = []
    for item in all_chapters:
        ret_an.append({'title' : item.chapter_title,
            'chapter_id' : item.id})
    try:
        import simplejson as json
    except:
        import json
    data = json.dumps(ret_an)
    return HttpResponse(data)

@POST_ONLY
def type_ranking_list(request):
    types = request.POST.get('type', '')
    try:
        fiction = Fiction.objects.filter(fiction_style = types).order_by('-rec_time', '-click_time')[:10]
    except:
        print 'no such one'
    try:
        import simplejson as json
    except:
        import json
    out = []
    for item in fiction:
        out.append({'intro' : item.fiction_intro[:40] + "",
            'avatar' : item.fiction_avatar_url,
            'nid' : item.fiction_nid,
            'source' : WEB_SITE[item.source_site.title]['name'],
            'author' : item.author,
            'title' : item.fiction_title})
    return HttpResponse(json.dumps(out))

@POST_ONLY
def get_category_number(request):
    ret = {}
    datas = ['1', '2', '22', '4', '5', '6', '7', '8', '9', '10', '12','14', '31', '41', '21', '15']
    for item in datas:
        ret[item] = Fiction.objects.filter(fiction_style = item).count()
    try:
        import simplejson as json
    except:
        import json
    out = []
    out.append(ret)
    return HttpResponse(json.dumps(out))

@POST_ONLY
def get_chapter_url(request):
    if request.method == 'GET':
        return HttpResponse('method not allowed')
    
    chapter_id = request.POST.get('chapter_id', '')
    try:
        chapter = Chapter.objects.get(id = chapter_id)
    except:
        return HttpResponse('no')
    ret = []
    for item in chapter.all_urls.all():
        ret.append({'title' : WEB_SITE[item.name]['name'],
            'url' : item.url,
            'frm' : item.name})
    try:
        import simplejson as json
    except:
        import json
    return HttpResponse(json.dumps(ret))
        
def category(request):
    if request.method == 'GET':
        category = request.GET.get('category', '0')
        sort_type = request.GET.get('sort_by', '0')
        page_index = request.GET.get('page_index', '1')
    else:
        category = request.POST.get('category', '0')
        sort_type = request.POST.get('sort_by', '0')
        page_index = request.POST.get('page_index', '1')
        frm = request.POST.get('from', '')
    style = {'1' : '奇幻', '2' : '武侠', '22' : '仙侠', '4' : '都市', '5' : '历史', '6' : '军事', '7' : '游戏', '8' : '竞技',
            '9' : '科幻', '10' : '灵异', '12' : '同人', '14' : '图文', '31' : '文学', '41' : '女生', '21' : '玄幻', '15' :  '青春'} 
    page_index = int(page_index)
    if category == '0': 
        sort_type = int(sort_type)
        if sort_type == 0:#popular
            fictions = Fiction.objects.all().order_by('-click_time', '-rec_time')[(page_index - 1) * 10 : page_index * 10]
        else:#time
            fictions = Fiction.objects.all()[(page_index - 1) * 10 : page_index * 10]
        #if the request is from ajax
        if request.method == 'POST' and frm == 'ajax':
            ret = []
            for item in fictions:
                ret.append({'avatar_url' : item.fiction_avatar_url,
                    'nid' : item.fiction_nid,
                    'title' : item.fiction_title,
                    'author' : item.author,
                    'style' : style[item.fiction_style],
                    'style_id' : item.fiction_style,
                    'score' : item.grading_total / item.grading_number if item.grading_number != 0 else '0人评过',
                    'intros': item.fiction_intro[:70].encode('utf-8')})
            try:
                import simplejson as json
            except:
                import json
            return HttpResponse(json.dumps(ret))
        #from get request
        total = Fiction.objects.count()
        page_num = (total - 1) / 10 + 1
        for item in fictions:
            item.style = style[item.fiction_style]
            item.score=  item.grading_total / item.grading_number if item.grading_number != 0 else '0人评过'
        ret_dict = {'total' : page_num,
            'current' : page_index,
            'content' : fictions,
            'user' : request.user,
            'is_auth' : request.user.is_authenticated()
            }

        return RTR('category.html', ret_dict, context_instance = RequestContext(request))
    else:
        if not style.has_key(category):
            return RTR('category.html', {'NO' : True})
        sort_type = int(sort_type)
        if sort_type != 1:#popular
            fictions = Fiction.objects.filter(fiction_style = category).order_by('-click_time', '-rec_time')[(page_index - 1) * 10 : page_index * 10]
        else:#time
            fictions = Fiction.objects.filter(fiction_style = category)[(page_index - 1) * 10 : page_index * 10]
        #if the request is from ajax
        if request.method == 'POST' and frm == 'ajax':
            ret = []
            cnt = Fiction.objects.filter(fiction_style = category).count() 
            if cnt == 0:
                ret.append(0)
            else:
                ret.append((cnt - 1) / 10 + 1)
            print ret
            for item in fictions:
                ret.append({'avatar_url' : item.fiction_avatar_url,
                    'nid' : item.fiction_nid,
                    'title' : item.fiction_title,
                    'author' : item.author,
                    'style' : style[item.fiction_style],
                    'style_id' : item.fiction_style,
                    'score' : item.grading_total / item.grading_number if item.grading_number != 0 else '0人评过',
                    'intros': item.fiction_intro[:70].encode('utf-8')})
            try:
                import simplejson as json
            except:
                import json
            print ret
            return HttpResponse(json.dumps(ret))

@POST_ONLY
def newest_catch(request):
    fictions = Fiction.objects.all()[:10]
    out = []
    for item in fictions:
        out.append({'nid' : item.fiction_nid,
            'title' : item.fiction_title,
            'from' : '',
            'intro' : item.fiction_intro[:38],
        })
    try:
        import simplejson as json
    except:
        import json
    return HttpResponse(json.dumps(out))

@POST_ONLY

def get_fiction_and_chapter(request):
    data = request.POST.get('data', '')
    try:
        import simplejson as json
    except:
    
        import json
    try:
        datas = json.loads('[' + data + ']')
    except:
        return HttpResponse('error')
    out = []
    datas.reverse()
    for item in datas[:10]:
        fiction_nid = item['fiction_nid']
        chapter_id = item['chapter_id']
        time = item['time']
        url = item['url']
        if not fiction_nid and not chapter_id:
            continue
        try:
            fiction = Fiction.objects.get(fiction_nid = fiction_nid)
        except Exception,e:
            continue
        try:
            chapter = Chapter.objects.get(id = chapter_id)
        except:
            
            try:
                chapter = fiction.all_chapters.all()[0]
            except:
                chapter = None

        ret = {}
        try:
            ret['chapter_title'] = chapter.chapter_title
        except:
            ret['chapter_title'] = ''
        ret['fiction_title'] = fiction.fiction_title
        ret['url'] = url
        ret['time'] = time
        ret['fiction_nid'] = fiction_nid
        ret['chapter_id'] = chapter_id
        ret['fiction_chapter'] = fiction.all_chapters.all()[0].chapter_title if fiction.all_chapters.all() else '无'
        out.append(ret)
    try:
        import simplejson as json
    except:
        import json
    return HttpResponse(json.dumps(out))
