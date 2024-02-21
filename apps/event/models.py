from django.db import models
from apps.category.models import Details as Category_details

class Details(models.Model): 
    id = models.AutoField(primary_key = True)
    event_name = models.CharField(max_length = 100, default = None)
    category = models.ForeignKey(Category_details, on_delete = models.CASCADE, related_name = "event_category_id") 
    price = models.IntegerField()
    event_date = models.DateField()
    publish_date = models.DateField()
    event_start_time = models.CharField(max_length = 100)