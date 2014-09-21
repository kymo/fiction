from django.db import models
from fiction.models import Fiction
# Create your models here.

"""self database"""
class Shelf(models.Model):
    fictions = models.ManyToManyField(Fiction, through = 'ShelfFictionRelationship')
    fiction_number = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table = 'shelf'
    

class ShelfFictionRelationship(models.Model):
    shelf = models.ForeignKey(Shelf)
    fiction = models.ForeignKey(Fiction)
    """
    status:
        0: see it but not add into the shelf
        1: add it into the shelf
    """
    status = models.CharField(max_length = 12)
    #rating
    score = models.FloatField()
    
