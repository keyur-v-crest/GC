from django.db import models
from django.utils import timezone

class Details(models.Model): 
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length = 100, default = None, null = True)
    donation_name = models.CharField(max_length = 100, default = None)
    donation_target = models.FloatField()
    donation_start_date = models.DateField()
    donation_end_date = models.DateField()
    donation_address = models.CharField(max_length = 1000, default = None, null = True)
    donation_city = models.CharField(max_length = 1000, default = None, null = True)
    donation_state = models.CharField(max_length = 1000, default = None, null = True)
    description = models.CharField(max_length = 1000, default = None, null = True)
    organizer_name = models.CharField(max_length = 1000, default = None, null = True)
    organizer_contact = models.CharField(max_length = 1000, default = None, null = True)
    organizer_image = models.CharField(max_length = 1000, default = None, null = True)
    category = models.ForeignKey("category.Details", on_delete = models.CASCADE, null = True)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)
    donation_create_by = models.ForeignKey("user.Details", on_delete = models.CASCADE, null = True, related_name = "donation_create_user")

    def save(self, *args, **kwargs): 
        self.updated_at = timezone.now() 
        super().save(*args, **kwargs) 