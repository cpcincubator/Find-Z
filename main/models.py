from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class Root(models.Model):
  title = models.CharField(max_length=100)
  avatar = models.CharField(max_length=100)

class Catagory(models.Model):
  title = models.CharField(max_length=100)
  avatar = models.CharField(max_length=100)
  root = models.ForeignKey(Root, on_delete=models.CASCADE)

class Tutorial(models.Model):
  title = models.CharField(max_length=100)
  avatar = models.CharField(max_length=100)
  provider = models.CharField(max_length=20)
  short_desc = RichTextField()
  desc = RichTextField()
  url = models.CharField(max_length=100)
  type = models.CharField(max_length=50)
  price = models.CharField(max_length=50, blank=True)
  is_active = models.BooleanField(default=False)
  timestamp = models.DateTimeField(auto_now_add=True) 
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)



