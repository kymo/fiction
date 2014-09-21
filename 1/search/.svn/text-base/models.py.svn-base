from django.db import models
from fiction.models import Fiction
# Create your models here.
# definition for index database
# the database of index structure just like

class Index(models.Model): 
    key = models.CharField(max_length = 128)
    fiction = models.ManyToManyField(Fiction ,through = 'IndexFictionRelationship')
    class Meta:
        db_table = 'indexes'

class SearchKeyWord(models.Model):
    time = models.DateTimeField(auto_now_add = True)
    words = models.CharField(max_length = 128)
    record_time = models.IntegerField(default = 0)
    out_number = models.IntegerField(default = 0)
    class Meta:
        db_table = 'search_key_word'

class SearchRecord(models.Model):
    key_word = models.ForeignKey(SearchKeyWord, related_name = 'all_records')
    ip = models.CharField(max_length = 128)
    total_word = models.TextField()
    time = models.DateTimeField(auto_now_add = True)
    recorder = models.CharField(max_length = 32, null = True)
    class Meta:
        db_table = 'search_record'

class IndexFictionRelationship(models.Model):    
    fiction = models.ForeignKey(Fiction)
    key = models.ForeignKey(Index)
    position = models.CharField(max_length = 100)
    """
        bit:
        1: fiction_title
        2: fiction_intro
        3: chapter
    """
    bit = models.CharField(max_length = 2)
    class Meta:
        db_table = 'index_fiction_relationship'
