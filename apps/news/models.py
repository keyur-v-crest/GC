from django.db import models

class Details(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(default = None, max_length = 1000)
    name = models.CharField(default = None, max_length = 200)
    news_type = models.CharField(default = None, max_length = 100)
    