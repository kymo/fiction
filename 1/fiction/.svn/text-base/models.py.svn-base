#encoding:utf-8
from django.db import models
# Create your models here.

class FictionWebSite(models.Model):
    """table definition for website"""
    title = models.CharField(max_length = 1024)
    url = models.CharField(max_length  = 1024)
    intro = models.TextField(max_length = 1024)
    current_visit_ip = models.TextField(max_length = 1024)
    current_visit_pv = models.TextField(max_length = 1024)
    total_visit_ip = models.TextField(max_length = 1024)
    total_visit_pv = models.TextField(max_length = 1024)
    class Meta:
        db_table = 'fiction_web_site'
        

class ChapterIndex(models.Model):
    fiction = models.IntegerField()
    web_site = models.CharField(max_length = 10)
    newest_index = models.IntegerField()
    class Meta:
        db_table = 'chapter_index'

class Tag(models.Model):
    tag = models.CharField(max_length = 128)

    class Meta:
        db_table = 'tag'
class Fiction(models.Model):
    """table definition for chapter"""
    fiction_title = models.CharField(max_length = 128, null = False)
    fiction_avatar_url = models.CharField(max_length = 1024)
    fiction_intro = models.TextField()
    fiction_nid = models.CharField(max_length = 16)
    web_sites = models.ManyToManyField(FictionWebSite, through = 'MemberShip')
    source_site = models.ForeignKey(FictionWebSite, related_name = 'all_records')
    tag = models.ManyToManyField(Tag)
    fiction_id = models.CharField(max_length = 128)
    total_word = models.CharField(max_length = 10)
    com_word = models.CharField(max_length = 10)
    stock_time = models.IntegerField()
    click_time = models.IntegerField(default = 0)
    rec_time = models.IntegerField(default = 0)
    grading_number = models.IntegerField(default = 0)
    grading_total = models.IntegerField(default = 0)
    author = models.CharField(max_length = 64)
    author_url = models.CharField(max_length = 256)
    """
    fictionstyle:
        1: 奇幻   8: 竞技 15:青春
        2: 武侠   9: 科幻
        22: 仙侠  10: 灵异
        4: 都市   12: 同人
        5: 历史   14: 图文
        6: 军事   31: 文学
        7: 游戏   41: 女生
        defined according to qidian.com
    """
    fiction_style = models.CharField(max_length = 20)
    class Meta:
        db_table = 'fiction'
        ordering = ['-id']
        unique_together = (("fiction_title", "author"))


class Chapter(models.Model):
    """table definition for chapter"""
    chapter_title = models.CharField(max_length = 255, null = False)
    fiction = models.ForeignKey(Fiction, related_name = 'all_chapters')
    charpter_url = models.CharField(max_length = 1024, null = False)
    source = models.ForeignKey(FictionWebSite, related_name = 'all_chapters')
    index = models.IntegerField()
    recommond_time = models.IntegerField(default = 0)
    record_time = models.DateTimeField(auto_now_add = True)
    """through
        0: from update thread
        1: from get_all thread
    """
    through = models.CharField(max_length = 2)
    class Meta:
        db_table = 'chapter'
        ordering = ['-id']
        unique_together = ("index", "fiction")

class NewestChapter(models.Model):
    chapter_title = models.CharField(max_length = 255, unique = True, null = False)
    fiction = models.ForeignKey(Fiction)
    charpter_url = models.CharField(max_length = 1024, null = False)
    source = models.ForeignKey(FictionWebSite)
    index = models.IntegerField()
    recommond_time = models.IntegerField(default = 0)
    record_time = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table = 'newest_chapter'
        ordering = ['-id']


class ChapterUrl(models.Model):
    url = models.CharField(max_length = 255, null = False, unique = True)
    chapter = models.ForeignKey(Chapter, related_name = 'all_urls')
    name = models.CharField(max_length = 1024)
    fiction = models.ForeignKey(Fiction, related_name = 'all_urls')
    index = models.IntegerField()
    title = models.CharField(max_length = 128)
    record_time = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table = 'chapter_url'
        ordering = ['-id']
        
class MemberShip(models.Model):
    """relationship between fiction and web_site"""
    fiction = models.ForeignKey(Fiction)
    website = models.ForeignKey(FictionWebSite)
    fiction_url = models.CharField(max_length = 128)
    class Meta:
        db_table = 'member_ship'
        
