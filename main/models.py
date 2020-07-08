from django.db import models
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from findZ.utils import *

class Root(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(max_length=50, null=True, blank=True)
  avatar = models.CharField(max_length=100)

class Catagory(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(max_length=50, null=True, blank=True)
  avatar = models.CharField(max_length=100)
  root = models.ForeignKey(Root, on_delete=models.CASCADE)
  

class Tutorial(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(max_length=50, null=True, blank=True)
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

def slug_generator(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Root)
pre_save.connect(slug_generator, sender=Catagory)
pre_save.connect(slug_generator, sender=Tutorial)