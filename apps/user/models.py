from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin 
from django.utils import timezone

class Details(AbstractUser, PermissionsMixin): 
    created_at = models.DateTimeField(auto_now_add = True )
    updated_at = models.DateTimeField(auto_now = True) 
    dob = models.CharField(max_length = 100, default = None) 
    address = models.CharField(max_length = 500, default = None, null = True)
    gender = models.CharField(max_length = 100)
    family_id = models.CharField(max_length = 100, default = None)
    profession = models.CharField(max_length = 100, default = None)
    profession_description = models.CharField(max_length = 500, default = None)

    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(**args, **kwargs)