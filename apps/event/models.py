from django.db import models
from apps.category.models import Details as Category_details
from apps.user.models import Details as User_details 
from django.utils import timezone

class Details(models.Model): 
    id = models.AutoField(primary_key = True)
    event_name = models.CharField(max_length = 100, default = None)
    event_description = models.CharField(max_length = 1000, default = None)
    category = models.ForeignKey(Category_details, on_delete = models.CASCADE, related_name = "event_category_id") 
    price = models.IntegerField()
    event_date = models.DateField()
    publish_date = models.DateField()
    event_start_time = models.CharField(max_length = 100)
    event_end_time = models.CharField(max_length = 100)
    event_address = models.CharField(max_length = 500, default = None)
    event_address_latitude = models.CharField(max_length = 100, default = None)
    event_address_longitude = models.CharField(max_length = 100, default = None)
    event_address_city = models.CharField(max_length = 100, default = None, null = True)
    event_address_state = models.CharField(max_length = 100, default = None, null = True)
    event_image = models.CharField(max_length = 100, default = None, null = True)
    number_of_seat = models.IntegerField(default = 0)
    organizer_name = models.CharField(max_length = 500, default = None)
    organizer_contact_number = models.CharField(max_length = 100, default = None)
    organizer_image = models.CharField(max_length = 1000, default = None, null = True)
    event_delete = models.BooleanField(default = False) 
    event_create_by = models.ForeignKey(User_details, on_delete=models.CASCADE, null = True)
    is_vip_seat = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)
    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs) 

class Booking(models.Model): 
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Details, on_delete = models.CASCADE)
    family_id = models.CharField(default = None, max_length = 500) 

class Gallery(models.Model): 
    id = models.AutoField(primary_key = True)
    event = models.ForeignKey(Details, on_delete = models.CASCADE, null = True, related_name = "event_images")
    type = models.CharField(max_length = 100, default = None)
    link = models.CharField(max_length = 1000, default = None)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)
    upload_by = models.ForeignKey("user.Details", on_delete = models.CASCADE, null = True)
    delete = models.BooleanField(default = False)

    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs) 
