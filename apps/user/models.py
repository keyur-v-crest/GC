from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin 
from django.utils import timezone
from djstripe.models import WebhookEventTrigger

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
    account_status = models.CharField(max_length = 100, default = None, null = True)

    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs)

class Event(models.Model): 
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey("user.Details", on_delete = models.CASCADE)
    event = models.ForeignKey("event.Details", on_delete = models.CASCADE) # event id information  
    family_id = models.CharField(max_length = 100, default = None, null = True) # family id 
    event_type = models.CharField(max_length = 100, default = None, null = True)
    book_by = models.ForeignKey(Details, on_delete=models.CASCADE, related_name = "book_user_id", null = True)
    status = models.CharField(max_length = 100, default = "Upcoming", null = True)
    ticket_number = models.CharField(max_length = 100, default = None, null = True) #ticket id 6digit random number 
    transaction_status = models.CharField(max_length = 100, null = True)
    payment = models.ForeignKey(WebhookEventTrigger, on_delete = models.CASCADE, null = True, related_name = "user_event_payment") # payment id reference information 
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)

    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs) 

class Donation(models.Model): 
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey("user.Details", on_delete = models.CASCADE)
    donation = models.ForeignKey("donation.Details", on_delete = models.CASCADE)
    transaction_status = models.CharField(max_length = 100, null = True)
    is_name_visible = models.BooleanField(default = True)
    payment = models.ForeignKey(WebhookEventTrigger, on_delete = models.CASCADE, related_name="user_donation_payment", null = True)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)

    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs) 


class Achievments(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey("user.Details", on_delete = models.CASCADE)
    name = models.JSONField(default = dict)
    count = models.IntegerField(default = 0)
    is_delete = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)

    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs) 