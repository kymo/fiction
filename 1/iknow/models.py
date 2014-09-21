from django.db import models

# Create your models here.

class Advice(models.Model):
    
    advice = models.TextField()
    frm = models.CharField(max_length = 128)
    time = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'advice'
