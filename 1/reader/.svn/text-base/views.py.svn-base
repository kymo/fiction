# Create your views here.
#encoding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response as RTR
from utils.hashs import create_nid
import hashlib
from django.contrib.auth import login, logout, authenticate
from reader.models import Account
from shelf.models import *
from fiction.models import *
from models import ReadLog, Feedback
#from validate import create_validate_code
import StringIO
from crawler.crawler_config import WEB_SITE
from search.views import POST_ONLY
from search.models import SearchKeyWord
from django.views.decorators.csrf import csrf_exempt
#route /register/

def validate(request):
    try:
        validate_code = create_validate_code()
    except:
        print 'error'
    request.session['validate'] = validate_code[1]
    mstream = StringIO.StringIO()
    img = validate_code[0]
    img.save(mstream, "GIF")
    return HttpResponse(mstream.getvalue(), "image/gif")

def not_legal(strs):
    if isinstance(strs, unicode):
        strs = strs.encode('utf-8')
    for item in strs:
        if ord(item) > 127:
            return True
    return False

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return RTR('register.html', {'error_msg' : False}, context_instance = RequestContext(request))
    #get validationg code
    validate_code = request.POST.get('validate', '')
    if not_legal(validate_code) or validate_code.lower() != request.session['validate'].lower():
        return RTR('register.html', {'error_msg' : True}, context_instance = RequestContext(request))
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    name = request.POST.get('name', '')
    remember = request.POST.get('remember', '')
    try:
        try:
            user = Account.objects.get(name = name)
            return HttpResponse("you ren le")
        except:
            pass
        #build shelf
        shelf = Shelf(fiction_number = 0)
        shelf.save()

        user = Account(name = name,
            password = hashlib.md5(password).hexdigest(),
            is_active = '0',
            email = email,
            shelf = shelf
            )
        user.save() 
        user.nid = create_nid(user.id)
        user.save()
        user = authenticate(name = user.name, password = password)
        if user:
            login(request, user)
            response = HttpResponseRedirect('/' + user.nid)
            if remember == 'on':
                response.set_cookie('login', 'True', max_age = 7 * 24 * 60 * 60)
            return response
        else:
            return HttpResponse('ok')
    except:
        HttpResponse("服务器故障,请稍候再试<a href = '%s'>返回<a/>" % request.META['HTTP_REFERER'])

@csrf_exempt
def check_name(request):
    if request.method == 'GET': 
        return HtttpResponse('Method Forbidden!')
    name = request.POST.get('name', '')
    try:
        user = Account.objects.get(name = name)
        return HttpResponse('YES')
    except:
        return HttpResponse('NO')

def add_shelf(request):
    fiction_id = request.POST.get('fiction_id', '')
    fiction = Fiction.objects.get(id = int(fiction_id))
    try:
        fiction.stock_time += 1
    except:
        fiction.stock_time = 1
    fiction.save()
    shelf = request.user.shelf
    shelf_fiction = ShelfFictionRelationship(shelf = request.user.shelf,
        fiction = fiction,
        status = '1',
        score = 0.0,
        )
    shelf_fiction.save()
    del shelf_fiction
    return HttpResponse('no')

def remove_shelf(request):
    fiction_nid = request.POST.get('fiction_nid', '')
    fiction = Fiction.objects.get(fiction_nid = fiction_nid)
    fiction.stock_time -= 1;
    fiction.save()
    shelf = request.user.shelf
    try:
        shelf_fiction = ShelfFictionRelationship.objects.get(shelf = request.user.shelf,
            fiction = fiction)
        shelf_fiction.delete()
        del shelf
        del fiction
        return HttpResponse('yes')
    except:
        return HttpResponse('no')
    
def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if 'GET' == request.method:
        return RTR('login.html', {}, context_instance = RequestContext(request))
    name = request.POST.get('name', '')
    password = request.POST.get('password' ,'')
    user = authenticate(name = str(name), password = str(password))
    if user:
        login(request, user)
        return HttpResponseRedirect('/' + user.nid)
    else:
        try:
            user = Account.objects.get(name = name)
        except:
            return RTR('login.html', {'msg' : '无此用户'}, context_instance = RequestContext(request)) 
        
        return RTR('login.html', {'msg' : '密码错误'}, context_instance = RequestContext(request))

def member(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/' + request.user.nid)
    else:
        return RTR('register.html', {'tips' : '注册启书,拥有电子书架，并能自动推荐你可能喜欢的小说.'}, context_instance = RequestContext(request))

def error(request):
    print 'error'
    return RTR('error.html', {})

def home(request, nid):
    if not request.user.is_authenticated():
        return HttpResponse('/login/')

    else:
        if nid != request.user.nid:
            return HttpResponseRedirect('/' + request.user.nid)

        #get shelfs' books
        try:
            ships = ShelfFictionRelationship.objects.filter(shelf = request.user.shelf)
        except:
            ships = []
        out = 0
        fiction = []
        style = {'1' : '奇幻', '2' : '武侠', '22' : '仙侠', '4' : '都市', '5' : '历史', '6' : '军事', '7' : '游戏', '8' : '竞技',
        '9' : '科幻', '10' : '灵异', '12' : '同人', '14' : '图文', '31' : '文学', '41' : '女生', '21' : '玄幻', '15' : '青春'}
        
        key = {}
        for item in ships:
            key[item.fiction.fiction_style] = 0
        style = {'1' : '奇幻', '2' : '武侠', '22' : '仙侠', '4' : '都市', '5' : '历史', '6' : '军事', '7' : '游戏', '8' : '竞技',
        '9' : '科幻', '10' : '灵异', '12' : '同人', '14' : '图文', '31' : '文学', '41' : '女生', '21' : '玄幻', '15' : '青春'}
        shelf_out, all_fics = [], []
        for tem in ships:
            all_fics.append(tem.fiction)
        
        for item in key.keys():
            fics = []
            for tem in ships:
                if tem.fiction.fiction_style == item:
                    fics.append(tem.fiction)
            shelf_out.append({'key' : style[item],
                'number' : len(fics),
                'id': item})
        out = []
        for item in key.keys():
            fictions = Fiction.objects.filter(fiction_style = item).order_by('-click_time', '-rec_time')[:100]
            click_time = 0
            for fics in fictions:
                breaks = False
                for temp in ships:
                    if fics.fiction_nid == temp.fiction.fiction_nid:
                        breaks = True
                        break
                    click_time += temp.fiction.click_time
            if not breaks:
                out.append({'key' : style[item], 'fictions' : fictions[:8], 'click_time' : click_time})
        out.sort(cmp = lambda x,y : -cmp(x['click_time'], y['click_time']))
        is_auth = True
        cdic =  {'user' : request.user, 
            'out' : out[:5], 
            'is_auth' : is_auth,
            'shelf_fic' : shelf_out, 
            'all' : all_fics[:40] }
        return RTR('home.html', cdic, context_instance = RequestContext(request))

def index(request):
    is_auth = request.user.is_authenticated()
    chapters = NewestChapter.objects.all()[:16]
    for item in chapters:
        item.url = item.charpter_url
        item.frm = WEB_SITE[item.source.title]['name']
        item.time = str(item.record_time)[:19]
        item.show_color = WEB_SITE[item.source.title]['color']
    
    user = request.user if is_auth else None
    fiction = Fiction.objects.all()[:30]
    fiction = list(fiction)
    fiction.sort(cmp = lambda x,y : -cmp(0.6 * x.rec_time + 0.4 * x.click_time, 
        0.6 * y.rec_time + 0.4 * y.click_time))
    fiction_word = fiction[6 : 12]
    fiction = fiction[:9]
    style = {'1' : '奇幻', '2' : '武侠', '22' : '仙侠', '4' : '都市', '5' : '历史', '6' : '军事', '7' : '游戏', '8' : '竞技',
        '9' : '科幻', '10' : '灵异', '12' : '同人', '14' : '图文', '31' : '文学', '41' : '女生', '21' : '玄幻', '15' : '青春'}
    for item in chapters:
        item.style = style[item.fiction.fiction_style.encode('utf-8')]
    
    try:
        hot_words = SearchKeyWord.objects.all().order_by('-record_time')[:5]
    except:
        hot_words = None
    
    fictions = Fiction.objects.all().order_by('-click_time')[:4]
    print fictions
    cdic =  {'chapter' : chapters, 
        'rec_fiction' : fiction, 
        'rec_fiction_word' : fiction_word,
        'is_auth' : is_auth, 
        'hot_words' : fictions,
        'user' : user}
    return RTR('index.html', cdic, context_instance = RequestContext(request)) 

@POST_ONLY
def save_read_log(request):
    log = request.POST.get('log', '')
    try:
        import simplejson as json
    except:
        import json
    ret = json.loads(log)
    
    for item in ret:
        if item['tag'] == '0':
            continue

        if item['fiction_nid']:
            try:
                fiction = Fiction.objects.get(fiction_nid = item['fiction_nid'])
            except:
                continue
            try:
                chapter = Chapter.objects.get(id = item['chapter_id'])
            except:
                try:
                    chapter = fiction.all_chapters.all()[0]
                except:
                    continue
            try:
                chapter = chapter[0]
                log = ReadLog.objects.get(reader = request.user, 
                    fiction =fiction, 
                    chapter = chapter)
                continue
            except:
                pass
            log = ReadLog(reader = request.user,
                fiction = fiction,
                chapter = chapter,
                chapter_url = item['url'],
                state = '1',#chapter is the newest one
                )
            log.save()
    return HttpResponse('.')

@POST_ONLY
def get_history(request):
    logs = request.user.all_logs.all()
    ret = []
    inx = 0
    for item in logs:
        ret.append({'fiction_title' : item.fiction.fiction_title,
            'fiction_nid' : item.fiction.fiction_nid,
            'id' : item.id,
            'chapter_title' : item.chapter.chapter_title,
            'time' : str(item.time),
            'chapter_url' : item.chapter_url,
            'is_new' : item.state})
        inx += 1
    print ret
    try:
        import simplejson as json
    except:
        import json
    return HttpResponse(json.dumps(ret))

@POST_ONLY
def del_history(request):
    ids = request.POST.get('id', '')
    read_log = ReadLog.objects.get(id = ids)
    read_log.delete()
    return HttpResponse('ok')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def helps(request): 
    ret = {'user' : request.user,
        'is_auth' : request.user.is_authenticated()}
    return RTR('help.html', '')

def feedback(request):
    if request.method == 'GET': 
        user = request.user
        is_auth = request.user.is_authenticated()
        ret = {'user' : user,
            'is_auth' : is_auth}
        return RTR('feedback.html', ret,  context_instance = RequestContext(request))

    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    feedback = request.POST.get('feedback', '')
    contact = request.POST.get('contact', '')

    feed = Feedback(feedback = feedback, 
        contact = contact,
        ip = ip)
    feed.save()
    return HttpResponse('/feedback/')
def contact(request):
    ret = {'user' : request.user,
        'is_auth' : request.user.is_authenticated()}

    return RTR('contact.html', ret)

def version(request):
    ret = {'user' : request.user,
        'is_auth' : request.user.is_authenticated()}

    return RTR('version.html', ret)

