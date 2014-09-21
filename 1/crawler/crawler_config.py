#encoding:utf-8
import re

#definition for crawler pattern

STYLE = {
    "qidian":
        {"东方玄幻" : "1", "异界征战" : "1", "异界大陆" : "1", "远古神话" : "1",
        "西方奇幻" : "21", "领主贵族" : "21", "亡灵骷髅" : "21", "异类兽族" : "21" ,"魔法校园" : "21",
        "传统武侠" : "2", "浪子异侠" : "2", "国术武技" : "2",
        "古典仙侠" : "22", "奇幻修真" : "22", "现代修真" : "22","洪荒封神" : "22",
        "都市生活" : "4" , "商战风云" : "4" ,"职场励志" : "4", "官场沉浮" : "4", "娱乐明星" : "4", "谍战特工" : "4",
        "恩怨情仇" : "4", "现实百态" : "4", "乡土小说" : "4", "合租情缘" : "4", "爱情婚姻" : "4", "异术超能" : "4",
        "青春校园" : "15", "校园异能" : "15",
        "架空历史" : "5", "上古先秦" : "5", "秦汉三国" : "5", "两晋隋唐": "5", "五代十国" : "5", "两宋元明" : "5", "清史民国" : '5', "外国历史" : "5", "历史传记" : "5",
        "军事战争" : "6", "抗战烽火" : "6", "战争幻想" : "6", "军旅生活" : "6",
        "游戏生涯" : "7", "虚拟网游" : "7", "电子竞技" : "7", "游戏异界" : "7",
        "体育竞技" : "8", "篮球运动" : "8", "足球运动" : "8", "弈林生涯" : "8",
        "未来世界" : "9", "星际战争" : '9', "古武机甲" : "9", "数字生命" : "9", "超级科技" : "9", "时空穿梭" : '9', "进化变异" : '9', "末世危机" : "9",
        "灵异奇谈" : "10", "恐怖惊悚" : "10", "推理侦探" : "10", "悬疑探险" : "10",
        "动漫同人" : "12", "武侠同人" : "12", "小说同人" : "12", "授权同人" : "12", "影视同人" : "12",
        "漫画连载" : "14", "配图小说" : "14", "四格幽默" : "14", "原画插画" : "14",
        "长篇参赛" : "31", "官场" : "31", "军事" : "31", "职场" : "31", "都市" : "31", "悬疑" : "31", "历史" : "31", "言情" :"31", "校园" : '31', '灵异' : '31', 
        '乡土' : '31', '社科' : '31', '纪实' : "31", "美文" : "31", "剧本" : '31', '科幻' : '31', "婚姻" : "31",
        "古代言情" : "41", "现代言情" : "41", "浪漫青春" : "41", "玄幻仙侠" : "41", "异界奇幻" : '41', "星际科幻" : '41', "游戏竞技" : '41' ,
        '灵异推理' : '41', '同人美文' : '41',
    },
    'xs8':
    {
        '都市高干' : '4', '豪门总裁' : '4', '穿越架空' : '5', '仙侠幻情' : '22',
        '纯爱耽美' : '41', '职场励志' : '4', '宫廷争斗' : '5', '种田重生' : '41', '青春校园' : '15', '灵异恐怖' : '10', '综合其他' : '4', '言情小本' : '41',
    },
    "630book":
    {
        "玄幻小说" : "1", "仙侠修真" : "2", "言情小说": "4","都市小说" : "4",
        "历史小说" : "6" , "网游小说" : "12", "科幻小说" : "9",
        "竞技小说" : "8", "全本小说" : "4"
        
    },
    "aoye":
    {
        "武侠仙侠" : "2", "玄幻奇幻" : "1", "都市言情"  : "4", "历史军事" : "6", "网游小说"  : "7",
        "竞技小说" : "8", "科幻灵异" : "9", "官场职场" : "4", "女生频道" : "41", "穿越小说" : "31", "其他类型" : "4"
    },
    "longtengzw":
    {
        "都市言情"  : "4", "玄幻魔法" :  "1", "武侠修真" : "2", "历史军事" : "6", 
        "网游动漫" : "7", "科幻小说" : "9", "恐怖灵异" : "10", "其他类型" : "4",
    }
}

#说明
#1. 进入网站书库页面
#   all_content_tag 为 提取当前页面所列小说信息的标签
#   all_content_dict 为 该标签的class或者id或者其他属性
#由上述两个标签，过滤了一部分信息，获取到了关键的当前页面的小说信息
#   all_fiction_tag 为 提取所列小说每一项的信息的标签
#   all_fiction_dict 为上诉标签的属性值(class或者id或者其他)
#   
ALL_PATTERN  = {

    "qidian":
    {
        #for all fiction
        "all_content_tag" : "div",
        "all_content_dict" : {"class" : "twoleft"},
        "all_fiction_tag" : "div",
        "all_fiction_dict" : {"class" : re.compile(r"sw[1-2]")},
        #pattern for the target information
        "all_fiction_type" : r"bookstore\.aspx\?ChannelId=\d+\" class=\"hui2\">(?P<tips>.*?)</a>",
        "all_fiction_title" : r"/Book/\d+.aspx\" target=\"_blank\">(?P<tips>.*?)</a>",
        "all_fiction_url" : r"(?P<tips>/Book/\w+.aspx?)",
        "all_author_name" : r"me.qidian.com.* class=\"black\">(?P<tips>[\w\W]*?)</a>",
        'ids_pattern' : r"/Book/(?P<tips>\w*?).aspx",
        #for each fiction
        "content_tag" : "div",
        "content_dict" : {"class" : "bookshow like_box"},
        "avatar_pattern" : r"src=\"(?P<tips>http:.*?)\"",
        "intro_pattern" : [r"<div class=\"txt\">\W+<b.*>.*</b>(?P<tips>[\w\W]*)<span id=\"spanBambook",r"<div class=\"txt\">\W*(?P<tips>[\w\W]*)\W+</div>[\w\W]*本站郑重提醒：本故事纯属虚构"],
        "infor_content_pattern" : r"<div class=\"info_box\">[\w\W]*</div>\W+</div>\W+<div class=\"cont\" id=\"authordiv\"",
        "click_pattern" : r"totalClick\">(?P<tips>\d+)?",
        "rec_pattern" : r"totalRecommend\">(?P<tips>\d+)?",
        "total_pattern" : r"wordCount\">(?P<tips>\d+)?",
        "tag_pattern" : r"\?Tag=[\%\w]+\" target=\"_blank\">(?P<tips>\W+)</a>",
        "style_pattern" : r"genre\">(?P<tips>.*)?</span>",
    },
    "aoye":
    {
        #for all fiction
        "all_content_tag" : "div",
        "all_content_dict"  : {"id" : "waterfall"},
        "all_fiction_tag" : "div",
        "all_fiction_dict" : {"class" : "item"},
        #pattern for target information
        "all_fiction_type" : r"<br />(?P<tips>\W+)? /",
        "all_fiction_title" : r"alt=\"(?P<tips>\W+)?\"",
        "all_fiction_url" : r"\"(?P<tips>/\d+/)\"?",
        "all_author_name" : r"nickname\">(?P<tips>\W+)? /",
        "ids_pattern" : r"/(?P<tips>\d+)?/",
        #for each fiction
        "content_tag" : "div",
        "content_dict" : {"id" : "bookdetail"},
        #end
        "avatar_pattern" : r"src=\"(?P<tips>.*?)\" title",
        "intro_pattern" : [r"<div id=\"aboutbook\">([\w\W]*?)</div>"],
        "tag_pattern" : "noway",
        #extra
        "infor_content_tag" : "div",
        "infor_content_dict" : {"class" : "infonum"},
        #infor_content_pattern
        "infor_content_pattern" : r"",
        "click_pattern" : r"总读次数：(\d+)?",
        "rec_pattern" : r"总推荐票：(\d+)?",
        "total_pattern" : r"完成字数：约(.+)?万字",
        "style_pattern" : r"作品类型：(\W+)?</li>"
    },
    "xs8":
    {
        "ids_pattern" : r"/book/(?P<tips>\d+?)/",
        #for each fiction
        "content_tag" : "div",
        "content_dict" : {"class" : "focus_main"},
        #extra
        'infor_content_tag' : 'div',
        'infor_content_dict' : {'class' : 'bookinfo'},
        #end
        "avatar_pattern" : r"<div class=\"fengmian\"><img src=\"(?P<tips>.*)\" width=\"200\"",
        "intro_pattern" : [r"<div class=\"bookintro cont c_show\" id=\"BookIntro\">(?P<tips>[\w\W]*)<span class=\"bibtn\""],
        "infor_content_pattern" : r"<div class=\"bookinfo\">(?P<tips>[\w\W]*)</div>[\w\W]*<div class=\"wrapper\">",
        "click_pattern" : r"阅读：(?P<tips>[\d\,]+)",
        "rec_pattern" : r"推荐：(?P<tips>[\d\,]+)",
        "total_pattern" : r"字数：(?P<tips>[\d\,]+)",
        "tag_pattern" : r"<a href=\"http://s.xs8.cn/kw/.*\" target=\"_blank\">(?P<tips>.*)</a>",
        "style_pattern" : "作品类型：<a href=\"http://s.xs8.cn/kw/(?P<tips>\W*)\">",
    },
    "630book" :
    {
        #for all fiction
        "all_content_tag" : "div",
        "all_content_dict" : {"id" : "alist"},
        "all_fiction_tag" : "div",
        "all_fiction_dict" : {"id" : "alistbox"},
        #pattern for target information
        "all_fiction_type" : r"分类：(?P<tips>[\w\W]*?).*收藏",
        "all_fiction_title" : r"<div class=\"title\">[\w\W]*http://www.630book.com/shu/\d*.html\" title=\"(?P<tips>\W+?)\"[\w\W]*</h2>",
        "all_fiction_url" : r"(?P<tips>http://www.630book.com/shu/\d+.html?)",
        "all_author_name" : r"<span>作者：(?P<tips>.+?)</span>",
        #id of fiction
        "ids_pattern" : r"/shu/(?P<tips>\d+?).html",
           
        #for each fiction
        "content_tag" : "div",
        "content_dict" : {"id" : "bookdetail"},
        #end
        "avatar_pattern" : r"src=\"(?P<tips>.*jpg?)\"",
        "intro_pattern" : [r"<div id=\"aboutbook\">([\w\W]*?)</div>"],
        "tag_pattern" : r"noway", 
        #extra
        "infor_content_tag" : "div",
        "infor_content_dict" : {"class" : "infotitle"},
        #infor_content_pattern
        "infor_content_pattern" : r"",
        "click_pattern" : r"总点击数：(\d+)?",
        "rec_pattern" : r"总推荐数：(\d+)?",
        "total_pattern" : r"完成字数：(\d+)?",
        "style_pattern" : r"<a href=\"/list/\d+.html\" target=\"_blank\">(?P<tips>\W*?)</a>",
    },
    "longtengzw":
    {
       
        "ids_pattern" : r"(?P<tips>\d+?).html",
        #for each fiction
        "content_tag"  :"div",
        "content_dict" : {"class" : "articleInfo"},
        #end
        "avatar_pattern" : r"src=\"(?P<tips>.*\.jpg?)\"",
        "intro_pattern" : [r"<dd id=\"wrap\">(?P<tips>[\w\W]*?)</dd>"],
        "tag_pattern": r"noway",
        #extar
        "infor_content_tag" : "no",
        "infor_content_dict" : {},
        'read_pattern' : r"href=\"(?P<tips>http://www.longtengzw.com/files/article/html/\d+/\d+/?)\"",
        #infor_content_pattern
        "infor_content_pattern" : r"<p class=\"left\">(?P<tips>[\w\W]*?)</p>",
        "click_pattern" : r"已有<strong>(?P<tips>\d+?)</strong>人读过",
        "rec_pattern" : r"已有<strong>(?P<tips>\d+?)</strong>人推荐",
        "total_pattern" : r"已写了<strong>(?P<tips>\d+?)</strong>字",
        "style_pattern"  : r"属于<strong>(?P<tips>\W*?)</strong>",
    }

}


NEWEST_PATTERN = {
    "qidian" : 
    {
        #get chapter infor mation area
        "content_tag" : "div",
        "content_dict" : {'class' : 'gxlbbg', 'id' : 'divUpdate1'},
        #get each chapter's information
        "chapter_tag" : "div",
        "chapter_dict" : {'class' : re.compile(r"gxlbbg[5-6]$")},
        #get title, author, chapter, types, chapter_url, fiction_url of each chapter
        "title_pattern" : r"<a href=\"/Book/\w+.aspx\" target=\"_blank\">(?P<tips>.*)</a>.*<span class=\"gxlbbg[5-6]bfont\"",
        "author_pattern" : r"<a href=\"http://me.qidian.com/authorIndex\.aspx\?.*\".*target=\"_blank\".*>(?P<tips>.*)</a>",
        "chapter_pattern" : r"<span class=\"gxlbbg[5-6]bfont\"><a.*href=\"http://.*read.*\.qidian\.com/BookReader/.*aspx\" target=\"_blank\" class=\"hui2\">(?P<tips>.*)</a></span>",
        "types_pattern" : r"<div class=\"gxlbbg[5-6]a\"><a.*target=\"_blank\" class=\"hui2\">(?P<tips>.*)</a></div><div class=\"gxlbbg[5-6]b\"",
        "chapter_url_pattern" : r"<span class=\"gxlbbg[5-6]bfont\">[\w\W]*<a href=\"(?P<tips>.*)\" target=\"_blank\" class=\"hui2\"",
        "fiction_url_pattern" : r"<div class=\"gxlbbg[5-6]b\">[\w\W]*<a href=\"(?P<tips>.*)\" target=\"_blank\">",
    },
    "xs8":
    {
        #get chapter infor mation area
        "content_tag" : "div",
        "content_dict" : {'class' : 'h480 tab_cont show'},
        #get each chapter's information
        "chapter_tag" : "dl",
        "chapter_dict" : {},
        #get title, author, chapter, types, chapter_url, fiction_url of each chapter
        "title_pattern" : r"<span class=\"f14\">(?P<tips>.*)</span>",
        "author_pattern" : r"<a.*href=\"/author/\w+.html\".*title=\"(?P<tips>.*)\">",
        "chapter_pattern" : r"<a.*href=\"/book/\w+/readbook.html\".*title=\"(?P<tips>.*)\">",
        "types_pattern" : r"<a href=\"/channel-\w*.html\" target=\"_blank\">(?P<tips>\W*)</a>",
        "chapter_url_pattern" : "<dd class=\"chapter\">[\w\W]*<a target=\"_blank\" href=\"(?P<tips>/book.*)\" title=\".*\"",
        "fiction_url_pattern" : "<a target=\"_blank\" href=\"(?P<tips>/book/.*/index.html)\"", 
    },
    '630book':
    {
        #get chapter information area
        "content_tag" : "div",
        "content_dict" : {'id' : 'tlist'},
        #get each chapter
        "chapter_tag" : "li",
        "chapter_dict" : {},
        "types_pattern" : r"href=\"/list/\d+.html\" title=\"(?P<tips>\W+?)\"" ,
        "title_pattern" : r"/shu/\d+.html\" title=\"(?P<tips>\W*?)\"",
        "chapter_pattern" : r"/shu/\d+/\d+.html\" title=\"(?P<tips>.*?)\" target=\"_blank\"",
        "author_pattern" : r"title=\"(?P<tips>\W*?)作品集",
        "fiction_url_pattern" : r"href=\"(?P<tips>http://www.630book.com/shu/\d+.html)\"",
        "chapter_url_pattern" : r"href=\"(?P<tips>http://www.630book.com/shu/\d+/\d+.html)\"",
    },
    'longtengzw' : 
    {
        #get chapter information area
        "content_tag" : "ul",
        "content_dict" : {"id" : "a0a"},
        #get each chapter's information
        "chapter_tag" : "ol",
        "chapter_dict" : {},
        "types_pattern" : r"类别：(?P<tips>\W*?)</span>",
        "title_pattern" : r"indexliBookName\">(?P<tips>\W*?)</a>",
        "chapter_pattern" : r"target=\"_blank\">(?P<tips>.*?)</a></h2>",
        "author_pattern" :r"author=(?P<tips>.*?)\"",
        "fiction_url_pattern" : "href=\"(?P<tips>http://www.longtengzw.com/book/\d+\.html?)\" class",
        "chapter_url_pattern" : "href=\"(?P<tips>http://www.longtengzw.com/files/.*\.html?)\"",
    },
}

WEB_SITE = {
    'xs8' : {'name' : '言情小说吧'},
    'qidian' : {'name' : '起点中文网'},
    '630book' : {'name' : '630看书'},
    "aoye" : {"name" : '熬夜看书网'},
    "longtengzw" : {"name" : "龙腾中文网"},
}
