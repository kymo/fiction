from django.db import models
from shelf.models import Shelf
from fiction.models import Fiction, Chapter
import hashlib
# Create your models here.

class Account(models.Model):
    email = models.CharField(max_length = 64)
    password=  models.CharField(max_length = 64)
    name = models.CharField(max_length = 20)
    is_active = models.BooleanField()
    nid = models.CharField(max_length = 10)
    shelf = models.ForeignKey(Shelf, unique = True)
    def is_authenticated(self):
        return True

    def hashed_password(self, password = None):
        if not password:
            return self.password
        else:
            return hashlib.md5(password).hexdigest()

    def check_password(self, password):
        if self.hashed_password(password) == self.password:
            return True
        return False

    class Meta:
        db_table = 'account'
        
class Score(models.Model):
    score = models.IntegerField(default = 0)
    fiction = models.ForeignKey(Fiction, related_name = 'all_score_record')
    recoreder = models.ForeignKey(Account, related_name = 'all_scores')
    time = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table = 'score'


class Feedback(models.Model):
    feedback = models.CharField(max_length = 128)
    time = models.DateTimeField(auto_now_add = True)
    contact = models.CharField(max_length = 128)
    ip = models.CharField(max_length = 128)

    class Meta:
        db_table = 'feedback'

class ReadLog(models.Model):
    
    reader = models.ForeignKey(Account, related_name = "all_logs")
    time = models.DateTimeField(auto_now_add = True)
    fiction = models.ForeignKey(Fiction, related_name = "all_logs_fic")
    chapter = models.ForeignKey(Chapter, related_name = "all_log_chp")
    chapter_url = models.CharField(max_length = 128, null = True)
    state = models.CharField(max_length = 2, default = '0')
    class Meta:
        db_table = 'read_log'
