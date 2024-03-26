from django.db import models
from datetime import datetime
from django.utils import timezone

class Details(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(default = None, max_length = 1000)
    name = models.CharField(default = None, max_length = 200)
    news_type = models.CharField(default = None, max_length = 100)
    short_description = models.CharField(default = None, max_length = 1000, null = True)
    publish_date = models.DateField(null = True)
    description = models.TextField(null = True)
    author_name = models.CharField(default = None, max_length = 100, null = True)
    author_image = models.CharField(default = None, max_length = 100, null = True)
    is_active = models.BooleanField(default = False)
    count = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)
    create_by = models.ForeignKey("user.Details", on_delete = models.CASCADE, null = True, related_name = "news_create_user")
    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs) 