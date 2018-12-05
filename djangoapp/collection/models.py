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
    model_type = forms.ChoiceField(widget=forms.RadioSelect)
    #user - models.ForeignKey(User)
