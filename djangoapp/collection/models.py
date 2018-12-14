from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class Results(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)

class Post(models.Model):
    post = models.CharField(max_length=500)
    #model_type = forms.ChoiceField(widget=forms.RadioSelect)

class KnnRecommendation(models.Model):
    index = models.IntegerField(primary_key=True, blank=False, null=False)
    books = models.TextField(blank=True, null=True)
    recommendation_1 = models.TextField(blank=True, null=True)
    recommendation_2 = models.TextField(blank=True, null=True)
    recommendation_3 = models.TextField(blank=True, null=True)
    recommendation_4 = models.TextField(blank=True, null=True)
    recommendation_5 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'knn_recommendation'
