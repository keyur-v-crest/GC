from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin 
from django.utils import timezone

class Details(AbstractUser, PermissionsMixin): 
    created_at = models.DateTimeField(auto_now_add = True )
    updated_at = models.DateTimeField(auto_now = True) 
    dob = models.CharField(max_length = 100, default = None, null = True) 
    address = models.CharField(max_length = 500, default = None, null = True)
    gender = models.CharField(max_length = 100)
    family_id = models.CharField(max_length = 100, default = None, null = True)
    profession = models.CharField(max_length = 100, default = None, null = True)
    profession_description = models.CharField(max_length = 500, default = None, null = True)
    relation = models.CharField(max_length = 100, default = None, null = True)
    step1 = models.BooleanField(default = False)
    step2 = models.BooleanField(default = False)
    step3 = models.BooleanField(default = False)
    step4 = models.BooleanField(default = False)
    email_verified = models.BooleanField(default = False)
    mobile_verified = models.BooleanField(default = False)
    email_otp = models.CharField(default = None, max_length = 10, null = True)
    mobile_otp = models.CharField(default = None, max_length = 10, null = True)
    email_otp_expier = models.CharField(max_length = 100, default = None, null = True)
    mobile_otp_expier = models.CharField(max_length = 100, default = None, null = True) 
    mobile = models.CharField(max_length = 100, default = None, null = True)
    sub_member = models.BooleanField(default = False) 
    profile_image = models.CharField(null = True, max_length = 200, default = None)
    is_admin = models.BooleanField(default = False)

    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs)

class Event(models.Model): 
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey("user.Details", on_delete = models.CASCADE)
    event = models.ForeignKey("event.Details", on_delete = models.CASCADE) 
    family_id = models.CharField(max_length = 100, default = None, null = True)
    event_type = models.BooleanField(default = False)
    book_by = models.ForeignKey(Details, on_delete=models.CASCADE, related_name = "book_user_id", null = True)
    status = models.CharField(max_length = 100, default = "Upcoming", null = True)
    ticket_number = models.CharField(max_length = 100, default = None, null = True)

    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)

    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs) 