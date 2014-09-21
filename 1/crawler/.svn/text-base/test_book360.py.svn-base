#encoding:utf-8

from BeautifulSoup import BeautifulSoup
from crawler_config import NEWEST_PATTERN, ALL_PATTERN
import re

def test_book630():
    content = open('/home/kymo/Desktop/630book.newest.txt', 'r')
    html_page = content.read()
    content.close()
    html_page = BeautifulSoup(html_page)
    
    #tag and dict
    content_tag = NEWEST_PATTERN['630book']['content_tag']
    content_dict = NEWEST_PATTERN['630book']['content_dict']
    chapter_tag = NEWEST_PATTERN['630book']['chapter_tag']
    chapter_dict = NEWEST_PATTERN['630book']['chapter_dict']
    content = html_page.findAll(content_tag, content_dict)
    contents = ''.join([str(item) for item in content])
    chapter_infor = BeautifulSoup(contents)
    content = chapter_infor.findAll(chapter_tag, chapter_dict)
    print content

    #four patterns
    types_pattern = r"\[(?P<tips>\W*)\]" 
    title_pattern = r"免费阅读下载\">(?P<tips>\W*)</a> / <a style"
    chapter_pattern = r"target=\"_blank\">(?P<tips>.*)</a></div>[\w\W]*<div class=\"zz\""
    author_pattern =  "最全作品集\">(?P<tips>.*)</a></div>"
    
    fiction_url_pattern =  "href=\"(?P<tips>http://www.630book.com/book/\d+/)\""
    chapter_url_pattern =  "href=\"(?P<tips>http://www.630book.com/read/\d+/\d+/)\""

    for item in content:
        contents = str(item)
        print contents
        types = ''.join(re.findall(types_pattern, contents))
        title = ''.join(re.findall(title_pattern, contents))
        chapter = ''.join(re.findall(chapter_pattern, contents))
        author = ''.join(re.findall(author_pattern, contents))
        fiction_url = ''.join(re.findall(fiction_url_pattern, contents))
        chapter_url = ''.join(re.findall(chapter_url_pattern, contents))
        print types
        print title
        print chapter
        print author
        print fiction_url
        print chapter_url
if __name__ == '__main__':
    test_book630()
