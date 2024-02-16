from django.db import models
from django.utils import timezone

# Create your models here.

class Details(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length = 100, default = None)
    category_image = models.CharField(max_length = 1000, default = None)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs)
