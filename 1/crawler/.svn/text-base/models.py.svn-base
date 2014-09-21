from django.db import models
from fiction.models import Fiction
# Create your models here.

class Index(models.Model): 
    key = models.CharField(max_length = 128)
    fiction = models.ManyToManyField(Fiction ,through = 'IndexFictionRelationship')
    class Meta:
        db_table = 'indexes'

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

class HashUrl(models.Model):
    
    urls = models.CharField(max_length = 255, unique = True)

    class Meta:
        db_table = 'hash_url'
