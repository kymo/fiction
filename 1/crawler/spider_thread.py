#encoding:utf-8
#author: kades
#base thread definition for the spider engine


import threading
import urllib2
import re
try:
	from bs4 import BeautifulSoup
except:
    from BeautifulSoup import BeautifulSoup
from fiction.models import *
from models import *
"""
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
"""
import sys
from crawler import get_book_infor, get_chapters, get_chapter_630, chapter_func, build_url_fiction
from utils.hashs import create_nid
#load pattern
from crawler_config import NEWEST_PATTERN, STYLE, ALL_PATTERN

#to render the html page to get the content 
#which must be generated by javascript
"""
class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()
    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()
"""
#   spider thread
#   here we defined the newest html page three levels
#   first: the main content  of the newest area
#   second: the chapter area
#   third: the url area
#   after we render the html page with QtWebPage, we can get all the content
#   after saving the information into database, we need to segment the content and save them
#   into the index database

is_database_lock = False
class SpiderThread(threading.Thread):
    def __init__(self,
            thread_name = "",
            newest_url = "",
            newest_host = "",
            ):
        threading.Thread.__init__(self)
        
        self.thread_name = thread_name
        self.newest_url = newest_url
        self.host = newest_host
        
        pattern = NEWEST_PATTERN[self.thread_name]
        
        self.title_pattern = pattern["title_pattern"]
        self.author_pattern = pattern["author_pattern"]
        self.types_pattern = pattern["types_pattern"]
        self.chapter_pattern = pattern["chapter_pattern"]
        self.content_tag = pattern["content_tag"]
        self.content_dict = pattern["content_dict"]
        self.chapter_tag = pattern['chapter_tag']
        self.chapter_dict = pattern['chapter_dict']

        self.chapter_url_pattern = pattern['chapter_url_pattern']
        self.fiction_url_pattern = pattern['fiction_url_pattern']
    def rebuild_link(self, link):
        if link[0] == '/':
            return self.host + link

    def get_chapter_id(self, chapter):
        out_number = re.findall(r"(?P<tips>\d+)", chapter)
        if out_number:
            return int(out_number[0])
        st = re.findall(r"第(?P<tips>.*)章|第(?P<tips1>.*)回", chapter)
        if not st:
            return 10001
        num = ""
        for item in list(st[0]):
            if item:
                num = item
        number = self.getResultForDigit(num)
        return number

    def run(self):
        """thread method"""
        
        #get all the fresh information
        _headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",  
                     "Accept": "text/plain"} 
        print self.newest_url
        request = urllib2.Request(self.newest_url, headers = _headers)
        html_page = urllib2.urlopen(request).read() 
        try: 
            import gzip, StringIO
            data = html_page
            data = StringIO.StringIO(data)
            gzipper = gzip.GzipFile(fileobj=data)
            html = gzipper.read()
            html_page = html
        except:
            pass
        html_page = BeautifulSoup(str(html_page))
        content = html_page.findAll(self.content_tag, self.content_dict)
        contents = ''.join([str(item) for item in content])
        chapter_infor = BeautifulSoup(contents)
        content = chapter_infor.findAll(self.chapter_tag, self.chapter_dict)
        indexs = 1
        print content
        for item in content:
            indexs += 1
            contents = str(item)
            types = ''.join(re.findall(self.types_pattern, contents))
            title = ''.join(re.findall(self.title_pattern, contents))
            chapter = ''.join(re.findall(self.chapter_pattern, contents))
            author = ''.join(re.findall(self.author_pattern, contents))
            fiction_url = ''.join(re.findall(self.fiction_url_pattern, contents))
            chapter_url = ''.join(re.findall(self.chapter_url_pattern, contents))
            if not types or not title or \
                not chapter or not author or not fiction_url or not chapter_url:
                continue
            newest_chapter_url = chapter_url
            host = self.host
            print author
            if self.host[len(self.host) - 1] == '/':
                host = self.host[:len(self.host) - 1]
            if chapter_url[0] == '/':
                chapter_url = host + chapter_url
            if fiction_url[0] == '/':
                fiction_url = host + fiction_url
            try:
                web_site = FictionWebSite.objects.get(url = self.host)
            except:
                web_site = FictionWebSite(title = self.thread_name, url = self.host)
                web_site.save()
            try:
                hash_url = HashUrl.objects.get(urls = fiction_url)
                is_exit = True
                fic = Fiction.objects.get(fiction_title = title, author = author)
            except:
                is_exit = False
            print 'here'
            if not is_exit:
                try:
                    hash_url = HashUrl(urls = fiction_url)
                    hash_url.save()
                except:
                    continue
                #if the fiction got by crawler is the newest one
                #get the book infor
                book_infor = get_book_infor(self.host, self.thread_name, fiction_url, True)
                ids = re.findall(ALL_PATTERN[web_site.title]['ids_pattern'], fiction_url)
                types = '4' if not STYLE[self.thread_name].has_key(book_infor['types']) else \
                     STYLE[self.thread_name][(book_infor['types'])]
                try:
                    fic = Fiction(fiction_title = title, 
                        fiction_avatar_url = book_infor['avatar'],
                        fiction_intro = book_infor['intro'],
                        fiction_id = ids[0],
                        fiction_style = types,
                        total_word = book_infor['total_word'],
                        com_word = "",
                        source_site = web_site,
                        click_time = book_infor['click_time'],
                        rec_time = book_infor['rec_time'],
                        author = author,
                        stock_time = 0,
                        author_url = "",
                    )
                    fic.save() 
                    fic.fiction_nid = create_nid(fic.id)
                    fic.save()
                    member = MemberShip(fiction = fic, website = web_site, fiction_url = fiction_url)
                    member.save()
                    del member
                except Exception,e:
                    print 'Ever'
                    continue
                
                #search only by fiction title
                for item in mmseg.Algorithm(title):
                    try:
                        index = Index.objects.get(key = item.text)
                    except:
                        index = Index(key = item.text)
                        index.save()
                    IndexFictionRelationship.objects.create(key = index,
                        fiction = fic,
                        position = ','.join([str(item.start), str(item.end)]),
                        bit = '2',#chapter
                    )
                #get all chapters
                if book_infor.has_key('read_url'):
                    chapter_url = book_infor['read_url']
                else:
                    chapter_url = build_url_fiction(ids[0], web_site.title)
                get_chapters_thread = threading.Thread(target = chapter_func[web_site.title], 
                    args = (chapter_url, fic, web_site, '1'))
                get_chapters_thread.start()
                get_chapters_thread.join()
            #if the fiction has been inserted into the database before
            else:
                print "yes it is!"
                #get the max index of chapters
                try:
                    chapter_index = ChapterIndex.objects.get(fiction = fic.id, web_site = web_site.title)
                except Exception, e1:
                    try:
                        chapter_index = ChapterIndex.objects.filter(fiction = fic.id, web_site = web_site.title)[0]
                    except Exception, e:
                        print e
                    print e1
                    continue
                chapter_index.newest_index += 1
                chapter_index.save()
                #get the chapter
                try:
                    chap = Chapter.objects.get(fiction = fic, index = chapter_index.id)
                except:
                    chap = Chapter(chapter_title = chapter,
                        charpter_url = newest_chapter_url,
                        fiction = fic,
                        source = web_site,
                        index = chapter_index.newest_index,
                        through = '0',#from udpate thread
                        )
                    chap.save()
                try:
                    chapter_url = ChapterUrl.objects.get(url = chapter_url)
                except:
                    chapter_url = ChapterUrl(url = chapter_url,
                        chapter = chap,
                        fiction = fic,
                        index = chapter_index.newest_index,
                        name = web_site.title)
                    chapter_url.save()
                #save into newest chapter
                try:
                    NewestChapter.objects.create(chapter_title = chapter,
                        charpter_url = newest_chapter_url,
                        fiction = fic,
                        source = web_site,
                        index = chapter_index.newest_index,
                        )
                except:
                    continue
def qidian_test():
    """
    new_one = <div class="gxlbbg5"><div class="gxlbbg5a"><a href="http://gdyq.qdmm.com" target="_blank" class="hui2">[古代言情]</a></div><div class="gxlbbg5b"><a href="/Book/2572434.aspx" target="_blank">冠盖路</a> <span class="gxlbbg5bfont"><a rel="nofollow" href="http://vipreader.qidian.com/BookReader/vip,2572434,46281060.aspx" target="_blank" class="hui2">第一百八十五章 补偿</a></span> <span class="gxlbbg5bfont2">[VIP]</span></div><div class="gxlbbg5c"><a href="http://me.qidian.com/authorIndex.aspx?id=2600912" target="_blank" class="black">醉夜吟</a></div><div class="gxlbbg5d">06-27 14:21</div></div>
    strs = <div class="gxlbbg5"><div class="gxlbbg5a"><a href="http://xianxia.qidian.com" target="_blank" class="hui2">[仙侠]</a></div><div class="gxlbbg5b"><a href="/Book/2807393.aspx" target="_blank">仙炼乾坤</a> <span class="gxlbbg5bfont"><a href="http://read.qidian.com/BookReader/2807393,46280719.aspx" target="_blank" class="hui2">第一卷 修仙之始　第四十章 莫夫人</a></span> </div><div class="gxlbbg5c"><a href="http://me.qidian.com/authorIndex.aspx?id=3375302" target="_blank" class="black">龙猫骑士</a></div><div class="gxlbbg5d">06-27 13:56</div></div>
    tt = r"<div class=\"gxlbbg[5-6]a\"><a.*target=\"_blank\" class=\"hui2\">(?P<tips>.*)</a></div><div class=\"gxlbbg[5-6]b\""
    t2 = r"<a href=\"/Book/\w+.aspx\" target=\"_blank\">(?P<tips>.*)</a>.*<span class=\"gxlbbg[5-6]bfont\""
    t3 = r"<a href=\"http://me.qidian.com/authorIndex\.aspx\?.*\".*target=\"_blank\".*>(?P<tips>.*)</a>"
    t4 = r"<span class=\"gxlbbg[5-6]bfont\"><a.*href=\"http://.*read.*\.qidian\.com/BookReader/.*aspx\" target=\"_blank\" class=\"hui2\">(?P<tips>.*)</a></span>"
    ans = re.findall(t2, new_one)
    ans2 = re.findall(t4, strs)
    ans3 = re.findall(t3,strs)
    for item in ans:
        print item

    for item in ans2:
        print item
    for item in ans3:
        print item
    
    """
    st = SpiderThread('qidian',
        "http://www.qidian.com",
        "http://www.qidian.com",
        #four
        )
    st.start()
    print 'qidian thread start'

def xs8_test():
    st = SpiderThread('xs8', 
            "http://www.xs8.cn/",
            "http://www.xs8.cn/",
            )
    st.start()

def book630_test():
    st = SpiderThread('630book',
       "http://www.630book.com",
       "http://www.630book.com",
       )
    st.start()
    #get content

def longtengzw_test():
    st = SpiderThread('longtengzw',
    'http://www.longtengzw.com',
    'http://www.longtengzw.com')
    st.start()

if __name__ == '__main__':
    book630_test()