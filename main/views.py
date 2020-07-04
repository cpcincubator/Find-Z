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
    return render(request, 'main/index.html')


class Academic(View):
  def get(self, request):
    return render(request, 'main/academic.html')


class Programming(View):
  def get(self, request):
    return render(request, 'main/programming.html')


class Devops(View):
  def get(self, request):
    return render(request, 'main/devops.html')