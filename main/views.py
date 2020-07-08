from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from main.models import *
from adminpanel.form import *


class Index(View):
  def get(self, request):
    all_root = Root.objects.all()

    context ={
      'roots': all_root
    }
    return render(request, 'main/index.html', context)


class Catagories(View):
  def get(self, request, root_slug):
    root = Root.objects.filter(slug = root_slug)

    if root.exists():
      root = root.first()
      root_id = root.id
      all_catagory = Catagory.objects.filter(root_id = root_id)
    else:
      return render(request, 'main/404.html')

    context ={
      'root': root,
      'catagories': all_catagory
    }
    return render(request, 'main/catagories.html', context)


class Tutorials(View):
  def get(self, request, root_slug, catagory_slug):
    catagory = Catagory.objects.filter(slug = catagory_slug)

    if catagory.exists():
      catagory = catagory.first()
      catagory_id = catagory.id
      all_tutorial = Tutorial.objects.filter(catagory_id = catagory_id)
    else:
      return render(request, 'main/404.html')

    context ={
      'catagory': catagory,
      'tutorials': all_tutorial
    }
    return render(request, 'main/tutorials.html', context)

def not_found(request):
  return render(request, 'main/404.html')