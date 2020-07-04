from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class RootTutorial(models.Model):
  title = models.CharField(max_length=100)

class CatagoryTutorial(models.Model):
  title = models.CharField(max_length=100)
  root_tutorial = models.ForeignKey(RootTutorial, on_delete=models.CASCADE)

class Tutorial(models.Model):
  title = models.CharField(max_length=100)
  desc = RichTextField()
  catagory_tutorial = models.ForeignKey(CatagoryTutorial, on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  timestamp = models.DateTimeField(auto_now_add=True) 
  url = models.CharField(max_length=100)
  type = models.CharField(max_length=50)
  price = models.CharField(max_length=50, blank=True)
  is_active = models.BooleanField(default=False)
