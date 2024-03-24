from django.db import models
from django.utils import timezone

class Image(models.Model): 
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="image/")