#encoding:utf-8
import urllib2
from bs4 import BeautifulSoup
import re
import threading
from fiction.models import *
import string
from debug import Debug
from models import *
from utils.hashs import create_nid
#for the thread to crawler all the fiction information from qidian.com
from crawler_config import ALL_PATTERN
DG = Debug()
DG.debug = True


def get_book_infor(host,
    name,
    url,
    type_lock = False
   ):
    DG.trace('yes now')
    """get book information(avatar, introduction, click times, type, completed words number,
    and all the chapter in website:host

    Args:
        host: fiction website
        book_url: book url located in host
        content_tag: div area contains the fiction's information that we want
        content_class: indetification flags
        avatar_tag: the fictions' avatar
        avatar_class: indetification
        intro_tag, intro_class
    Return:
        {'avatar' : url,
        'type' : type,
        'intro' : introduction}
    """
    if url[0] == '/':
        if host[len(host) - 1] == '/':
            fiction_url = host + url[1:]
        else:
            fiction_url = host + url
    else:
        fiction_url = url
    """get the information of the fiction"""
    try:
        all_information_html = urllib2.urlopen(fiction_url)
    except Exception, e:
        DG.trace(e)

    all_content = all_information_html.read()
    all_content = gzip_content(all_content)
    pattern = ALL_PATTERN[name]
    #get the main content
    all_information_tag = BeautifulSoup(all_content)
    content_tag = all_information_tag.findAll(pattern['content_tag'], pattern['content_dict'])
    contents = ''.join([str(item) for item in content_tag])
    #get avatar url
    avatar_url = ''.join(re.findall(pattern['avatar_pattern'], contents))
    tags = re.findall(pattern['tag_pattern'], contents)
    #get introduction
    intro = ""
    for item in pattern['intro_pattern']:
        out = re.findall(item, contents)
        if out:
            intro = ''.join(out)
            break
    if not intro:
        return
    print 'yes yes yes'
    temp_str = re.findall(r"<script>(?P<tips>[\w\W]*?)</script>", intro)
    temp_str = ''.join([str(_item) for _item in temp_str])
    intro = string.replace(intro, temp_str, '')
    intro = BeautifulSoup(intro).getText()
    intro = string.replace(intro, '&nbsp;', '')
    intro = string.replace(intro, u'[+点此展开]', '')
    infor_content = ''.join(re.findall(pattern['infor_content_pattern'], contents)) 
    read_url = ""
    if pattern.has_key('read_pattern'):
        read_url = ''.join(re.findall(pattern['read_pattern'], contents))
    if infor_content == '':
        infor_tag = all_information_tag.findAll(pattern['infor_content_tag'], pattern['infor_content_dict'])
        infor_contents = infor_content.join([str(item) for item in infor_tag])
        infor_content = infor_contents
    contents = infor_content
    #get type
    print contents
    types = ""
    if type_lock:
        types = ''.join(re.findall(pattern['style_pattern'], contents)[:1])
    #get click time, rec_time ,total_word and tags
    click_time = ''.join(re.findall(pattern['click_pattern'], infor_content)) 
    rec_time = ''.join(re.findall(pattern['rec_pattern'], infor_content))
    total_word = ''.join(re.findall(pattern['total_pattern'], infor_content))
    click_time = string.replace(click_time, ',', '')
    rec_time = string.replace(rec_time, ',', '')
    total_word = string.replace(total_word, ',', '')
    #if the pattern has read_pattern
    if rec_time == '':
        rec_time = '0'
    if total_word == '':
        total_word = '0'
    if click_time == '':
        click_time = '0'
    if not avatar_url or not intro:
        return None
    ret = {'avatar' : avatar_url,
        'intro' : intro,
        'click_time' : click_time,
        'rec_time' : rec_time,
        'total_word' : total_word,
        'tags' : tags,
        'types' : types,
        }
    if read_url:
        ret['read_url'] = read_url
    return ret
def get_chapters(chapter_url, fic, web_site, frm = '0'): 
    content_tag = "div"
    content_class = {"class" : "list"}
    chapter_tag = "li"
    chapter_class = {}
    #build index
    html_page = urllib2.urlopen(chapter_url)
    html_content = html_page.read()
    ans = []
    #get content
    
    content = BeautifulSoup(html_content)
    content_fiction = content.findAll("div", {"class" : "box_cont"})
    len1 = len(content_fiction)
    content_fiction = content_fiction[1 : len1 - 1]
    content_fic = ''.join([str(item) for item in content_fiction])
    content = BeautifulSoup(content_fic)
    print content
    out = content.findAll(content_tag, content_class)
    contents = ''.join([str(item) for item in out])
    chapters = BeautifulSoup(contents).findAll(chapter_tag, chapter_class)
    for item in chapters:
        try:
            item_str = str(item)
        except:
            item_str = unicode(item).encode('utf-8')
        item_tag = BeautifulSoup(item_str)
        try:
            url = item_tag.a['href']
            if 'http' not in url and url[0] != '/':
                url = chapter_url + url
            chapter_title = item_tag.getText()
        except:
            continue
        ans.append((url, chapter_title))
    print ans
    if not ans:
        fic.delete()
        return
    save_chapter(ans, fic, web_site, frm)

def get_chapter_630(chapter_url, fic, web_site, frm = '0'):
    content_tag = "div"
    content_class = {"class" : "zjbox"}
    chapter_tag = "dd"
    chapter_class = {}
    #build index
    html_page = urllib2.urlopen(chapter_url)
    html_content = html_page.read()
    ans = []
    #get content
    content = BeautifulSoup(html_content)
    out = content.findAll(content_tag, content_class)
    contents = ''.join([str(item) for item in out])
    chapters = BeautifulSoup(contents).findAll(chapter_tag, chapter_class)
    for item in chapters:
        item_str = str(item)
        if isinstance(item, unicode):
            item_str = item.encode('utf-8')
        item_tag = BeautifulSoup(item_str)
        if item_tag.a:
            url = item_tag.a['href']
            chapter_title = item_tag.getText()
            ans.append((url, chapter_title))
    if not ans:
        fic.delete()
    save_chapter(ans, fic, web_site, frm)

def gzip_content(html_content):
    """解压页面为gzip编码的html页面"""
    try: 
        import gzip, StringIO
        data = StringIO.StringIO(html_content)
        gzipper = gzip.GzipFile(fileobj = data)
        return gzipper.read()
    except:
        return html_content

def get_chapter_xs8(chapter_url, fic, web_site, frm = '0'):
    """获取xs8的某篇小说的所有的章节信息"""
    content_tag = "div"
    content_class = {"class" : "mod_container"}
    chapter_tag = "li"
    chapter_class = {}
    html_page = urllib2.urlopen(chapter_url)
    html_content = html_page.read()
    ans = []
    html_content = gzip_content(html_content)
    content = BeautifulSoup(html_content)
    out = content.findAll(content_tag, content_class)
    contents = ''.join([str(item) for item in out])
    chapters = BeautifulSoup(contents).findAll(chapter_tag, chapter_class)
    for item in chapters:
        item_str = str(item)
        item_tag = BeautifulSoup(item_str)
        if item_tag.a:
            url = item_tag.a['href']
            chapter_title = item_tag.getText()
            ans.append((url, chapter_title))
    save_chapter(ans, fic, web_site, frm)

def get_chapter_aoye(chapter_url, fic, web_site, frm = '0'):
    """获取xs8的某篇小说的所有的章节信息"""
    content_tag = "div"
    content_class = {"id" : "detaillist"}
    chapter_tag = "li"
    chapter_class = {}
    html_page = urllib2.urlopen(chapter_url)
    html_content = html_page.read()
    ans = []
    html_content = gzip_content(html_content)
    content = BeautifulSoup(html_content)
    out = content.findAll(content_tag, content_class)
    contents = ''.join([str(item) for item in out])
    chapters = BeautifulSoup(contents).findAll(chapter_tag, chapter_class)
    for item in chapters:
        item_str = str(item)
        item_tag = BeautifulSoup(item_str)
        if item_tag.a:
            url = item_tag.a['href']
            chapter_title = item_tag.getText()
            ans.append((url, chapter_title))
    save_chapter(ans, fic, web_site, frm)

def get_chapter_longtengzw(chapter_url, fic, web_site, frm = '0'):
    """获取龙腾中文网的某篇小说的所有的章节信息"""
    content_tag = "div"
    content_class = {"class" : "readerListShow"}
    chapter_tag = "td"
    chapter_class = {"class" : "ccss"}
    html_page = urllib2.urlopen(chapter_url)
    html_content = html_page.read()
    ans = []
    html_content = gzip_content(html_content)
    content = BeautifulSoup(html_content)
    out = content.findAll(content_tag, content_class)
    contents = ''.join([str(item) for item in out])
    chapters = BeautifulSoup(contents).findAll(chapter_tag, chapter_class)
    for item in chapters:
        item_str = str(item)
        item_tag = BeautifulSoup(item_str)
        if item_tag.a:
            url = item_tag.a['href']
            url = chapter_url + url
            chapter_title = item_tag.getText()
            ans.append((url, chapter_title))
    save_chapter(ans, fic, web_site, frm)
    

chapter_func = {'qidian' : get_chapters, 
    '630book' : get_chapter_630,
    'xs8' : get_chapter_xs8,
    'aoye' : get_chapter_aoye,
    'longtengzw' : get_chapter_longtengzw}

def build_index_database(key, fic, pos):
    """build index
    
    Args:
        key: the content which gona to be segmented
        fic: fiction object which contains the key
        pos: position of the key word in fiction

    Return:
        None
    """
    try:
        words = mmseg.Algorithm(key)
    except Exception, e:
        return
    chn = "，？。《》）（、；“”’‘"
    for item in words:
        if item.text in chn:
            continue
        try:
            index = Index.objects.get(key = item.text)
        except:
            index = Index(key = item.text)
            index.save()
        index_fiction = IndexFictionRelationship(key = index,
            fiction = fic,
            position = ','.join([str(item.start), str(item.end)]),
            bit = pos, #fiction title)
        )
        index_fiction.save()

def build_url_chapter(url ,web_site):
    """ build url for each chapter
        accourding to the web_site
    """
    if web_site.title == 'qidian':
        if 'vip' in url:
            if url[0] == '/':
                url = "http://vipreader.qidian.com" + url
        else:
            if url[0] == '/':
                url = "http://read.qidian.com" + url
    elif web_site.title == '630book':
        url = 'http://www.630book.com' + url
    elif web_site.title == 'xs8':
        url = url
    elif web_site.title == 'aoye':
        url = 'http://www.aoye.cc' + url
    return url

def is_title_match(title1, title2):
    title1 = string.replace(title1, '&nbsp;', '')
    title2 = string.replace(title2, '&nbsp;', '')
    t1, t2 = "", ""
    for item in title1:
        if not ord(item) >= 0 or not ord(item) <= 127:
            t1 += item
    for item in title2:
        if not ord(item) >= 0 or not ord(item) <= 127:
            t2 += item
    title1, title2 = t1, t2
    if isinstance(title1, str):
        title1 = title1.decode('utf-8')
    if isinstance(title2, str):
        title2 = title2.decode('utf-8')
    cnt, f = 0, []
    len1 = len(title1)
    len2 = len(title2)
    for i in range(len1 + 1):
        f.append([])
        for j in range(len2 + 1):
            f[i].append(0)
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if title1[i - 1] == title2[j - 1]:
                f[i][j] = f[i - 1][j - 1] + 1
            else:
                f[i][j] = max(f[i - 1][j], f[i][j - 1])
    
    ratio1 = len1 - f[len1][len2]
    ratio2 = len2 - f[len1][len2]
    print ratio1, ratio2
    if ratio1 < 1 or ratio2 < 1:
        return True
    return False

def save_chapter(chapter_infor, fic, web_site, frm):
    """save the chapters which is in the fiction
    
    Args:
        chapter_infor: a dict contains the chapters' information
        fic: fiction object
        web_site: website object
    Return:
        None
    """
    print chapter_infor
    index = 0
    for url, title in chapter_infor:
        url = build_url_chapter(url, web_site)
        try:
            chapter_index = ChapterIndex.objects.get(fiction = fic.id, web_site = web_site.title)
        except Exception, e:
            chapter_index = ChapterIndex(fiction = fic.id,
                web_site = web_site.title,
                newest_index = 0)
            chapter_index.save()
        chapter_id = chapter_index.newest_index
        chapter_index.newest_index = chapter_id + 1
        chapter_index.save()
        index = chapter_index.newest_index
        #需要
        """
        chapter = None
        try:
            all_chapters = fic.all_chapters.all()
        except Exception,e:
            print e

        if all_chapters:
            for item in all_chapters:
                if is_title_match(item.chapter_title, title):
                    chapter = item
                    break
        if not all_chapters or not chapter:
        """
        try:
            chapter = Chapter(chapter_title = title,
                charpter_url = url,
                fiction = fic,
                source = web_site,
                index = chapter_id + 1,
                through = '1',#from get_all thread
                )
            chapter.save()
        except Exception, e:
            print e
            chapter = Chapter.objects.get(fiction = fic, index = chapter_id + 1)
        try:
            chapter_url = ChapterUrl.objects.get(url = url)
        except:
            chapter_url = ChapterUrl(url = url,
                chapter = chapter,
                fiction = fic,
                title = title,
                index = chapter_id + 1,
                name = web_site.title)
            chapter_url.save()
    if frm == '1':#如果保存的是抓取最新的章节
        try:
            newest_chapter_url, chapter = chapter_infor[len(chapter_infor) - 1]
            NewestChapter.objects.create(chapter_title = chapter,
                charpter_url = newest_chapter_url,
                fiction = fic,
                source = web_site,
                index = chapter_index.newest_index,
            )
        except:
            pass

def build_url_fiction(ids, web_site):
    if web_site == 'qidian':
        chapter_url = "http://read.qidian.com/BookReader/%s.aspx" % (ids)
    elif web_site == '630book':
        chapter_url = "http://www.630book.com/shu/%s.html" % (ids)
    elif web_site == 'xs8':
        chapter_url = "http://www.xs8.cn/book/%s/readbook.html" % (ids)
    elif web_site == 'aoye':
        chapter_url = "http://www.aoye.cc/%s/" % ids
    elif web_site == 'longtengzw':
        chapter_url = "http://www.longtengzw.com/book/%s.html" % ids
    return chapter_url

def build_url_page(url,
    web_site,
    index,
    types):
    if web_site == 'qidian':
        new_url = url + "?PageIndex=%s&ChannelId=%s" % (str(index), types)
    elif web_site == '630book':
        new_url = url + "%s/%s.html" % (types, str(index))
    elif web_site == 'aoye':
        TYPE = {"1" : "1", "2" : "2", "4" : "3", "6" : "4", "7" : "5", "8" : "6",
        "9" : "7", "41" : "9", "31" : "10"}
        new_url = url + "%s_0_0_0_%s.html" %(TYPE[types], str(index)) 
    return new_url


def crawler_types(types, 
        web_site, 
        url,    
        ):      
    #index stands for the pageIndex
    pattern = ALL_PATTERN[web_site.title]

    for index in range(1, 100):
        new_url = build_url_page(url, web_site.title, index, types)
        html_page = urllib2.urlopen(new_url)
        html_content = html_page.read()
        html_content = gzip_content(html_content)
        #get content
        content = BeautifulSoup(html_content)
        out = content.findAll(pattern['all_content_tag'], pattern['all_content_dict'])
        if not out:
            break
        contents = ''.join([str(item) for item in out])
        chapter = BeautifulSoup(contents)
        fictions = chapter.findAll(pattern['all_fiction_tag'], pattern['all_fiction_dict'])
        for item in fictions:
            #get fiction title
            contents = str(item)
            try:
                fiction_title = re.findall(pattern['all_fiction_title'], contents)
                fiction_title = ''.join([str(_item) for _item in fiction_title])
                #get fiction url
                fiction_url = re.findall(pattern['all_fiction_url'], contents)
                fiction_url = ''.join([str(_item) for _item in fiction_url[0]])
                #get fiction type
                fiction_type = re.findall(pattern['all_fiction_type'], contents)
                fiction_type = ''.join([str(_item) for _item in fiction_type])
                #get fiction id in thissite
                author_name = re.findall(pattern['all_author_name'], contents)
                author_name = ''.join([str(_item) for _item in author_name])
                ids = re.findall(pattern['ids_pattern'], fiction_url)
                if not fiction_title or not fiction_url or not author_name:
                    continue
                #get write information 
            except Exception,e:
                continue
            try:
                hash_url = HashUrl.objects.get(urls = fiction_url)
                continue
            except:
                hash_url = HashUrl(urls = fiction_url)
                hash_url.save()

            fiction_infor = get_book_infor(web_site.url,
                web_site.title,
                fiction_url,    
            )
            if not fiction_infor:
                continue
            #save tag
            #save all the fiction into database
            try:
                #如果同样的标题的小说已经被收录,唯一性由标题和作者确定
                fic = Fiction.objects.get(fiction_title = fiction_title,author = author_name)
                #如果所在网站相同，则不继续处理
                DG.trace("get it")
                if fic.source_site.title == web_site.title:
                    continue

            except:
                fic = Fiction(fiction_title = fiction_title,
                    fiction_avatar_url = fiction_infor['avatar'],
                    fiction_intro = fiction_infor['intro'],
                    fiction_id = ids[0],
                    fiction_style = types,
                    total_word=  fiction_infor['total_word'],
                    stock_time = 10,
                    com_word = "",
                    source_site = web_site,
                    click_time = fiction_infor['click_time'],
                    rec_time = fiction_infor['rec_time'],
                    author = author_name,
                    author_url = "",
                )
                fic.save()
                fic.fiction_nid = create_nid(fic.id)
                fic.save()
                if isinstance(fiction_title, unicode):
                    fiction_title = fiction_title.encode('utf-8')
                #如果是新加入的小说，则为其建立索引
                #t1 = threading.Thread(target = build_index_database, args = (fiction_title, fic, '1'))
                #t1.start()
                #t1.join()
            #save tags
            for tags in fiction_infor['tags']:            
                try:
                    tag = Tag.objects.get(tag = tags)
                except:
                    tag = Tag(tag = tags)
                    tag.save()
                fic.tag.add(tag)
                fic.save()
            #新添小说和网站的联系表
            ms = MemberShip(fiction = fic, website = web_site, fiction_url = fiction_url)
            ms.save()
            #获取该小说的所有章节
            chapter_url = build_url_fiction(ids[0], web_site.title)
            t2 = threading.Thread(target = chapter_func[web_site.title], args = (chapter_url, fic, web_site))
            t2.start()
            t2.join()


def test_crawler(fiction_url):
    fiction_infor = get_book_infor('http://qidian.com',
        'qidian',
        fiction_url,
        )
    if not fiction_infor:
        return
    print fiction_infor
    #save tag
    #save all the fiction into database
    fiction_title = '武炼巅峰'
    author_name = '莫默'
    ids = ['2494758']
    types = '1'
    try:
        web_site = FictionWebSite.objects.get(title = 'qidian')
    except:
        web_site = FictionWebSite(title = 'qidian',
            url = 'http://qidian.com',
            )
        web_site.save()
    try:
        #如果同样的标题的小说已经被收录,唯一性由标题和作者确定
        fic = Fiction.objects.get(fiction_title = fiction_title,author = author_name)
        #如果所在网站相同，则不继续处理
        DG.trace("get it")
        print fic.source_site.title
        print web_site.title
        if fic.source_site.title == web_site.title:
            return
    except Exception,e:
        print e
        fic = Fiction(fiction_title = fiction_title,
            fiction_avatar_url = fiction_infor['avatar'],
            fiction_intro = fiction_infor['intro'],
            fiction_id = ids[0],
            fiction_style = types,
            total_word=  fiction_infor['total_word'],
            stock_time = 10,
            com_word = "",
            source_site = web_site,
            click_time = fiction_infor['click_time'],
            rec_time = fiction_infor['rec_time'],
            author = author_name,
            author_url = "",
        )
        fic.save()
        fic.fiction_nid = create_nid(fic.id)
        fic.save()
        if isinstance(fiction_title, unicode):
            fiction_title = fiction_title.encode('utf-8')
        #如果是新加入的小说，则为其建立索引
        t1 = threading.Thread(target = build_index_database, args = (fiction_title, fic, '1'))
        t1.start()
        t1.join()
    #save tags
    for tags in fiction_infor['tags']:            
        try:
            tag = Tag.objects.get(tag = tags)
        except:
            tag = Tag(tag = tags)
            tag.save()
        fic.tag.add(tag)
        fic.save()
    #新添小说和网站的联系表
    ms = MemberShip(fiction = fic, 
        website = web_site, 
        fiction_url = build_url_fiction(ids[0], web_site.title))
    ms.save()
    
    #获取该小说的所有章节
    chapter_url = build_url_fiction(ids[0], web_site.title)
    print chapter_url
    t2 = threading.Thread(target = chapter_func[web_site.title], args = (chapter_url, fic, web_site))
    t2.start()
    t2.join()


def qidian_crawler():
    """crawler all the fictions in qidian.com"""

    """
    chapter_url = "http://read.qidian.com/BookReader/%s.aspx" % ("2594550")
    print chapter_url
    chapter_infor = get_chapters(chapter_url,
        "div",
        {"class" : "list"},
        "li",
        {})

    """
    try:
        web_site = FictionWebSite.objects.get(title = 'qidian')
    except:
        web_site = FictionWebSite(title = 'qidian',
            url = 'http://qidian.com',
            )
        web_site.save()
    threads = []
    style = ['1', '21', '2', '22', '4', '5', '6', '7', '8', '9', '10', '12', '14', '31', '15']
    for types in style:
        url = "http://all.qidian.com/book/bookStore.aspx"
        t = threading.Thread(target = crawler_types, args = (types, web_site, url))
        t.start()
        threads.append(t)
    
    for item in threads:
        item.join()

def book630_crawler():
    """
    pass
    """
    try:
        web_site = FictionWebSite.objects.get(title = '630book')
    except:
        web_site = FictionWebSite(title = '630book',    
            url = 'http://www.630book.com',
            )
        web_site.save()
    threads = []
    style = ['1', '2', '4', '6', '8', '12', '9']
    for types in style[0]:
        url = "http://www.630book.com/list/"
        t = threading.Thread(target = crawler_types, args = (types, web_site, url))
        t.start()
        threads.append(t)

    for item in threads:
        item.join()

def aoye_crawler():
    """crawler aoye website"""
    try:
        web_site = FictionWebSite.objects.get(title = 'aoye')
    except:
        web_site = FictionWebSite(title = 'aoye',    
            url = 'http://www.aoye.cc',
            )
        web_site.save()
    threads = []
    style = ['1', '2', '4', '6', '7', '8', '9', '31']
    for types in style[:1]:
        url = "http://www.aoye.cc/type/"
        t = threading.Thread(target = crawler_types, args = (types, web_site, url))
        t.start()
        threads.append(t)

    for item in threads:
        item.join()

def xs8_crawler():
    """crawler all the fictions in xs8.cn"""

function_dict = {"qidian" : qidian_crawler,
    "xiaoshuosousuo" : xs8_crawler}
"""


                    
                #chapter_url 
                chapter_url = "read.qidian.com/BookReader/%s.aspx" % str(ids[0])
            
            #check if the fiction has been inserted into database
            #get the fiction's information
            """
"""

if __name__ == '__main__':
    function_dict["qidian"]()
    print get_book_infor("http://qidian.com",
        "/Book/2843691.aspx",
        "div", #content_tag
        {"class" : "bookshow like_box"}, #content_class
        "div", #avatar_tag
        {"class" : "pic_box"}, #avatar_class
        "div", #intro_tag
        {"class" : "txt"}, #intro_class,
        "div", #click_tag
        {"class" : "data"}, #click_class
        r"<b>总点击.*</b>(?P<tips>\d+)", #cick_pattern
        "div", #rec_tag
        {"class" : "data"}, #rec_class
        r"<b>总推荐.*</b>(?P<tips>\d+)",
        "div", #total_tag
        {"class" : "data"}, #total_class
        r"<b>总字数.*</b>(?P<tips>\d+)", #total_pattern
        "div", #com_tag
        {"class" : "info_box"}, #com_class
        r"<b>完成字数.*</b>(?P<tips>\d+)", #com_pattern
        )
"""
