from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

class Register(View):
  def post(self, request):
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]

    try:
      if User.objects.filter(username=username).exists():
        user_data={"error":True,"errorMessage":"Username already taken!"}
        return JsonResponse(user_data, safe=False)

      elif User.objects.filter(email=email).exists():
        user_data={"error":True,"errorMessage":"Already have an account with this email!"}
        return JsonResponse(user_data, safe=False)
              
      else:
        user = User.objects.create_user(username = username, email = email, password = password, is_active = False)
        user_data={'id':user.id,'username':user.username,'email':user.email,"error":False,"errorMessage":"Signed Up Successfully!"}
        return JsonResponse(user_data, safe=False)

    except:
      user_data = {"error":True,"errorMessage":"Server Error!"}
      return JsonResponse(user_data, safe=False)



class Login(View):
  def post(self, request):
    username = request.POST['username']
    password = request.POST['password']
        
    user = auth.authenticate(username=username, password=password)

    try:            
      if user is not None:
        if not user.is_active:
          login_data = {"error":True,"errorMessage":"Your account is not active yet!"}
          return JsonResponse(login_data, safe=False)
          
        auth.login(request, user)
        if request.GET:
          return redirect(request.GET['next'])
        return redirect('/')
           
      else:
        login_data = {"error":True,"errorMessage":"Invalid Credentials!"}
        return JsonResponse(login_data, safe=False)      

    except:
      login_data = {"error":True,"errorMessage":"Server Error!"}
      return JsonResponse(login_data, safe=False)


def logout(request):
  auth.logout(request)
  return redirect('/')