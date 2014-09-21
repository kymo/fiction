
#encoding:utf-8
import re



st = """<div class="txt">
 <b style="color: Red; display: none" id="essactive">[新人写作季作品]</b>
  
   　　诡谲的通商之路，几千代大公子的性命与鲜血，铸就了御苍左界修者的通天之路，也注定了七大世商冠绝左界的豪富地位与悲凉的命途；又一代世商子弟的成人，传承的却是七族命运多舛的开始。
   <br>&nbsp;&nbsp;&nbsp;     既川神碑的现世，角山祖殿的逆返；左臂蛇尊的飞腾，带动了既川神域与方天神域之间的上古迷团！
   <br>&nbsp;&nbsp;&nbsp;     林琪瑢没有前路！但他知道唯有不断前行，他才能有活路；
   <br>&nbsp;&nbsp;&nbsp;     他的诉求如此简单，简单的就跟别人放个屁一样；他从来没有想过，在无意间却筑就了一条属于他自己的离奇曲折的巅峰之路……
    
     <span id="spanBambookPromotion" style="color: red; display: none;">&nbsp;&nbsp;&nbsp;&nbsp;<a href="http://bbtg.sdo.com/0" target="_blank" style="color: Red;">读网络文学就用盛大Bambook，多款优惠套装官网促销中！</a></span>
      </div>
    """

import string
#get avatar_url

sts = """
<div class="bookshow like_box">
 <div class="box_title2">
  <div class="page_site">
   <a href="/">起点女生网首页</a> &gt; 
    <a href="http://gdyq.qdmm.com/">古代言情</a> &gt;
     <a target="_blank" href="http://all.qdmm.com/MMWeb/BookStore.aspx?ChannelId=71&amp;SubCategoryId=329">权谋朝争 </a> &gt; 
      <a href="/MMWeb/2696378.aspx">隋隅而安</a> 
       <i>(书号2696378)</i>
        </div>
         <div class="book_domain_name">
          本书域名：http://2696378.qdmm.com
           <a href="javascript:;" onclick="ShowBook.AddBookMark()">加入收藏</a>
            </div>
             </div>
              <div class="box_cont">
               <div class="book_pic">
                <div class="pic_box">
                 <a href="/BookReader/2696378.aspx">
                  <img onerror="this.onerror=null;this.src='http://image.cmfu.com/Books/0.jpg';" src="http://image.cmfu.com/books/2696378/2696378.jpg" alt="《隋隅而安》作者：张冉雅"></a></div>
                   <div class="opt">
                    <ul>
                     <li><a href="/BookReader/2696378.aspx" title="点击阅读">点击阅读</a></li>
                      <li><a href="javascript:;" onclick="ShowBook.AddBookCase();return false;" title="加入书架">
                       加入书架</a></li>
                        <li><a href="javascript:;" onclick="PageHandler.ShowBook.ShowPoP.Show('poptj');return false;" title="投推荐票">投推荐票</a></li>
                         <li id="ctl00_MainZonePart_li_pink" style="display:none"><a href="javascript:;" onclick="PageHandler.ShowBook.ShowPoP.Show('poppink');return false;" title="投月票" style="letter-spacing: 2px;">投粉红月票</a></li>
                          <li><a href="javascript:;" onclick="PageHandler.ShowBook.DownLoadPop('down');return false;" title="下载阅读">下载阅读</a></li>
                           <li><a href="javascript:;" id="ctl00_MainZonePart_li_DaShang" class="active" onclick="PageHandler.ShowBook.ShowPoP.Show('popds');return false;" title="打赏作品">打赏作品</a></li>
                            <li id="li_preBookOrder" style="display:none"><a href="javascript:;" onclick="pageHandle.PreBookOrderDo();return false;" title="预定实体版" class="st"> 预定实体版</a></li>
                             
                              
                               
                                </ul>
                                 </div>
                                  </div>
                                   <div class="book_info">
                                    <div class="title"> 
                                     
                                      <strong>
                                       隋隅而安</strong>
                                        <b>小说作者：</b>
                                         <a target="_blank" href="http://me.qdmm.com/authorIndex.aspx?id=3045504">
                                          张冉雅</a> 
                                           <a href="javascript:;" id="authortitleCount" style="display:none" target="_blank"></a>
                                            <div id="adandroid">
                                             <a title="起点官方阅读器" href="http://c.qidian.com/" target="_blank" style="margin-right: 235px;">
                                              <img height="25" width="140" src="/Images/btnandriod02.gif" alt="起点官方手机阅读器">
                                               </a>
                                                </div>
                                                 </div>
                                                  
                                                   <div class="tabs">
                                                    <ul>
                                                     <li><a href="javascript:;" class="active" onclick="ShowBook.Switch('BookInfo',this);return false;" onmouseover="ShowBook.Switch('BookInfo',this);return false;" id="contenttitle">内容介绍</a></li>
                                                      <li><a href="javascript:;" onclick="ShowBook.Switch('BookInfo',this);return false;" onmouseover="ShowBook.Switch('BookInfo',this);return false;" id="booktitle" class="">作品信息</a></li>
                                                       <li><a href="javascript:;" onclick="ShowBook.Switch('BookInfo',this);ShowBook.DisplayAuthorOtherBook();return false;" onmouseover="ShowBook.Switch('BookInfo',this);ShowBook.DisplayAuthorOtherBook();return false;" id="authortitle" class="">作者信息</a></li>
                                                        <li><a href="javascript:;" onclick="ShowBook.Switch('BookInfo',this);return false;" onmouseover="ShowBook.Switch('BookInfo',this);ShowBook.SwitchLoadIframe('ifmrolediv','http://baike.qidian.com/Iframe/BookRolesPop.aspx?bookId=2696378');return false;" title="隋隅而安作品角色" id="roletitle" style="color:Red;" class="">作品角色</a> </li>
                                                         <li><a href="javascript:;" onclick="ShowBook.Switch('BookInfo',this);return false;" id="sotitle" style="display: none" class="">SO大展</a></li>
                                                          </ul>
                                                           <div class="right">
                                                            更新时间：2013-07-01 13:37</div>
                                                             </div>
                                                              <div class="cont" id="contentdiv" style="">
                                                               <div class="intro">
                                                                <!-- 书介绍 -->
                                                                 
                                                                  <div class="txt">
                                                                   &nbsp;&nbsp;&nbsp;&nbsp;<br>&nbsp;&nbsp;&nbsp;&nbsp;无妄一穿，直抵隋末之乱。我是个婴孩，荣华淡去，事事成殇。<br>&nbsp;&nbsp;&nbsp;&nbsp;再度重生年华散落，岁月催去，我们相爱成虐。<br>&nbsp;&nbsp;&nbsp;&nbsp;乱世里的迂回脚步太乱，但我还记得，那轻落的蛩音里，第一眼见你，我心正有初雪。<br>&nbsp;&nbsp;&nbsp;&nbsp;
                                                                    </div>
                                                                     <div>&nbsp;&nbsp;&nbsp;&nbsp;(本站郑重提醒：本故事纯属虚构，如有雷同，纯属巧合，切勿模仿。)</div>
                                                                      </div>
                                                                       </div>
                                                                        <div class="cont" style="display: none; " id="bookdiv">
                                                                         <div class="info_box">
                                                                          <!-- 作品信息 -->
                                                                           <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                                                            <tbody><tr>
                                                                             <td height="20">
                                                                              <b>小说性质：</b>VIP作品
                                                                               </td>
                                                                                <td>
                                                                                 <b>总点击：</b>8279
                                                                                  </td>
                                                                                   <td>
                                                                                    <b>月点击：</b>261
                                                                                     </td>
                                                                                      <td>
                                                                                       <b>周点击：</b>261
                                                                                        </td>
                                                                                         </tr>
                                                                                          <tr>
                                                                                           <td height="20">
                                                                                            <b>小说类别：</b><a href="http://gdyq.qdmm.com/" target="_blank">权谋朝争</a>
                                                                                             </td>
                                                                                              <td>
                                                                                               <b>总推荐：</b>202
                                                                                                </td>
                                                                                                 <td>
                                                                                                  <b>月推荐：</b>0
                                                                                                   </td>
                                                                                                    <td>
                                                                                                     <b>周推荐：</b>0
                                                                                                      </td>
                                                                                                       </tr>
                                                                                                        <tr>
                                                                                                         <td height="20">
                                                                                                          <b>写作进程：</b>情节展开
                                                                                                           </td>
                                                                                                            <td>
                                                                                                             <b>完成字数：</b>273678
                                                                                                              </td>
                                                                                                               <td>
                                                                                                                <b>授权状态：</b><strong>
                                                                                                                 Ａ级签约
                                                                                                                  </strong>
                                                                                                                   </td>
                                                                                                                    <td>
                                                                                                                     <b class="red">
                                                                                                                      本书起点女生网首发</b>
                                                                                                                       </td>
                                                                                                                        </tr>
                                                                                                                         </tbody></table>
                                                                                                                          <div class="honour" style="display: none;">
                                                                                                                           暂无相关荣誉
                                                                                                                            </div>
                                                                                                                             </div>
                                                                                                                              <div style="padding:12px;">
                                                                                                                               
                                                                                                                                <div>
                                                                                                                                 
                                                                                                                                  </div>
                                                                                                                                   </div>
                                                                                                                                    </div>
                                                                                                                                     <div class="cont" id="authordiv" style="display: none; ">
                                                                                                                                      <div class="author_info">
                                                                                                                                       <h3>
                                                                                                                                        作者的话：</h3>
                                                                                                                                         <div class="hua">
                                                                                                                                          点击好不给力啊，小小心酸，喜欢的亲们藏一藏吧，你们的喜欢是我最大的动力哟!其实真的是个好故事，原谅我厚脸皮吧。不信的亲们，跟我来哟！
                                                                                                                                           </div>
                                                                                                                                            <h3>
                                                                                                                                             作者的其它作品：</h3>
                                                                                                                                              <div class="opus" id="authorOtherBookDiv"><div class="box"><div class="pic"><a href="/MMWeb/2488791.aspx" title="贼心晃晃"><img alt="贼心晃晃" src="http://image.cmfu.com/books/2488791/2488791.jpg" width="50" height="63"></a></div><div class="opuscont"><a href="/MMWeb/2488791.aspx"><b>贼心晃晃</b></a><br>字数：682898<br>类别：<a href="http://xhxx.qdmm.com/">东方玄幻</a></div></div></div>
                                                                                                                                               </div>
                                                                                                                                                </div>
                                                                                                                                                 <div class="cont" id="rolediv" style="display: none; ">
                                                                                                                                                  <iframe id="ifmrolediv" name="ifmrolediv" frameborder="0" width="100%" height="100%" scrolling="no">&lt;img src="../Images/bg_rem_title.gif" /&gt; </iframe>
                                                                                                                                                   </div>
                                                                                                                                                    <div class="cont" id="sodiv" style="display: none; ">
                                                                                                                                                     <div class="so_exhibition">
                                                                                                                                                      <!-- SO大展 -->
                                                                                                                                                       <span style="font-size: 14px; color: Red"><strong>
                                                                                                                                                        
                                                                                                                                                         </strong></span>
                                                                                                                                                          <br>
                                                                                                                                                           <strong>
                                                                                                                                                            </strong>类参展作品<br>
                                                                                                                                                             综合得分<span style="font-size: 12px; color: Red;"><strong></strong></span>分 排名<span style="font-size: 12px; color: Red"><strong>
                                                                                                                                                              </strong><br>
                                                                                                                                                               <img height="15" border="0" alt="hot" width="28" src="http://cj.qidian.com/svnad/images/hot2_090715.gif"><a style="font-size: 14px; color: Red" target="_blank" href="http://www.qidian.com/ploy/20100418/"><strong>专题：全球写作大展（SO）盛典隆重举行</strong>
                                                                                                                                                                </a><a style="font-size: 14px; color: Red" target="_blank" href="http://bbs.qidian.com/list/33">
                                                                                                                                                                 <strong>论坛</strong></a><br>
                                                                                                                                                                  
                                                                                                                                                                   </span>
                                                                                                                                                                    </div>
                                                                                                                                                                     </div>
                                                                                                                                                                      <div class="other">
                                                                                                                                                                       <div id="ctl00_MainZonePart_divAddLabel" class="editlabels">
                                                                                                                                                                        <a href="javascript:;" onclick="PageHandler.ShowBook.ShowPoP.Show('popbq');return false;">添加印象</a>
                                                                                                                                                                         </div>
                                                                                                                                                                          <div class="labels">
                                                                                                                                                                           <div class="box">
                                                                                                                                                                            <table border="0" cellspacing="0" cellpadding="0" width="100%" height="95">
                                                                                                                                                                             <tbody>
                                                                                                                                                                              <tr>
                                                                                                                                                                               <td>
                                                                                                                                                                                <b>小说类别：</b><a href="http://gdyq.qdmm.com/" target="_blank">权谋朝争</a>
                                                                                                                                                                                 </td>
                                                                                                                                                                                  <td>
                                                                                                                                                                                   <span class="red"><b>长评积分：</b>0</span>
                                                                                                                                                                                    
                                                                                                                                                                                     </td>
                                                                                                                                                                                      </tr>
                                                                                                                                                                                       <tr>
                                                                                                                                                                                        <td>
                                                                                                                                                                                         <span class="item"><b>总点击：</b>8279
                                                                                                                                                                                          </span>
                                                                                                                                                                                           </td>
                                                                                                                                                                                            <td>
                                                                                                                                                                                             </td>
                                                                                                                                                                                              </tr>
                                                                                                                                                                                               <tr>
                                                                                                                                                                                                <td>
                                                                                                                                                                                                 <span class="item"><b>总推荐：</b>202
                                                                                                                                                                                                  </span>
                                                                                                                                                                                                   </td>
                                                                                                                                                                                                    <td>
                                                                                                                                                                                                     <span class="item"><b>授权状态：</b><strong class="red">
                                                                                                                                                                                                      Ａ级签约
                                                                                                                                                                                                       </strong>
                                                                                                                                                                                                        </span>
                                                                                                                                                                                                         </td>
                                                                                                                                                                                                          </tr>
                                                                                                                                                                                                           <tr>
                                                                                                                                                                                                            <td>
                                                                                                                                                                                                             <span class="item"><b>总字数：</b>273678
                                                                                                                                                                                                              </span>
                                                                                                                                                                                                               </td>
                                                                                                                                                                                                                <td>
                                                                                                                                                                                                                 <strong>本书起点女生网首发</strong>
                                                                                                                                                                                                                  </td>
                                                                                                                                                                                                                   </tr>
                                                                                                                                                                                                                    </tbody>
                                                                                                                                                                                                                     </table>
                                                                                                                                                                                                                      </div>
                                                                                                                                                                                                                       <div class="box">
                                                                                                                                                                                                                        <b>作者</b>自定义标签：<br>
                                                                                                                                                                                                                         &nbsp;
                                                                                                                                                                                                                          <a href="http://all.qdmm.com/MMWeb/BookStore.aspx?Tag=%e7%a9%bf%e8%b6%8a" target="_blank">穿越</a>、<a href="http://all.qdmm.com/MMWeb/BookStore.aspx?Tag=%e5%ae%ab%e6%96%97" target="_blank">宫斗</a>、<a href="http://all.qdmm.com/MMWeb/BookStore.aspx?Tag=%e8%8b%a6%e6%81%8b" target="_blank">苦恋</a><br>&nbsp;&nbsp;<a href="http://all.qdmm.com/MMWeb/BookStore.aspx?Tag=%e6%9d%83%e8%b0%8b" target="_blank">权谋</a>、<a href="http://all.qdmm.com/MMWeb/BookStore.aspx?Tag=%e5%94%af%e7%be%8e" target="_blank">唯美</a>
                                                                                                                                                                                                                           <br>
                                                                                                                                                                                                                            <b>读者</b>印象：<br>
                                                                                                                                                                                                                             &nbsp;
                                                                                                                                                                                                                              <a href="http://sosu.qidian.com/searchresult.aspx?searchkey=%E5%A5%BD%E4%B9%A6&amp;searchtype=%E4%B8%BB%E8%A7%92" target="_blank">好书</a><i>(3)</i>、<a href="http://sosu.qidian.com/searchresult.aspx?searchkey=%E5%BE%88%E6%A3%92&amp;searchtype=%E4%B8%BB%E8%A7%92" target="_blank">很棒</a><i>(1)</i>、<a href="http://sosu.qidian.com/searchresult.aspx?searchkey=%E7%BB%8F%E5%85%B8%E5%B0%8F%E8%AF%B4&amp;searchtype=%E4%B8%BB%E8%A7%92" target="_blank">经典小说</a><i>(1)</i>
                                                                                                                                                                                                                               </div>
                                                                                                                                                                                                                                </div>
                                                                                                                                                                                                                                 </div>
                                                                                                                                                                                                                                  </div>
                                                                                                                                                                                                                                   </div>
                                                                                                                                                                                                                                    </div>
                                                                                                                                                                                                                """
#avatar_url = re.findall(r"<div class=\"book_pic\">\W+<div class=\"pic_box\">\W+<a href=\"/Book/\d+.aspx\">\W+<img src=\"(?P<tips>.*)\" alt=\".*\" onerror=\".*\"", teag)
#get intro
intro = re.findall(r"<div class=\"txt\">\W+<b.*>.*</b>(?P<tips>[\w\W]*)<span id=\"spanBambook", sts)
from BeautifulSoup import BeautifulSoup
intro = BeautifulSoup(''.join(intro)).getText()
intro = string.replace(intro, "&nbsp;", " ")
print '.'
aout = re.findall(r"<div class=\"txt\">\W+(?P<tips>[\w\W]*)\W+</div>[\w\W]*本站郑重提醒：本故事纯属虚构", sts)
#get book infro content
print aout

av = re.findall(r"<div class=\"book_pic\">\W*<div class=\"pic_box\">\W+<a href=\"/Book\w*/\d+.aspx\">\W+<img.*src=\"(?P<tips>.*)\"", sts)
print av
"""
contents_book = ''.join(re.findall(r"<div class=\"info_box\">[\w\W]*</div>\W+</div>\W+<div class=\"cont\" id=\"authordiv\"", teag))
click_time = re.findall(r"总点击：</b>(?P<tips>\d+)", contents_book)
rec_time = re.findall(r"总推荐：</b>(?P<tips>\d+)", contents_book)
total_word = re.findall(r"完成字数：</b>(?P<tips>\d+)", contents_book)
types = re.findall(r"小说类别：</b><a href=\".*\" target=\"_blank\">(?P<tips>\W+)</a>", teag)
tags = re.findall(r"\?Tag=[\%\w]+\" target=\"_blank\">(?P<tips>\W+)</a>\W+", teag)

print ''.join(types).decode('utf-8')
print types
print tags
aot = re.findall(r"<//b>(?P<tips>[\n.]*)<span id = \"spanBambook", st)
aots = re.findall(r"</b>(?P<tips>[\n\w\W]*)<span", st)
for item in aots:
    item = string.replace(item, '<br>' ,'')
"""
