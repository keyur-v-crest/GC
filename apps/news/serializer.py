from rest_framework import serializers
from apps.news.models import Details as News_model 

class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News_model
        fields = ["id", "name", "short_description", "image"]