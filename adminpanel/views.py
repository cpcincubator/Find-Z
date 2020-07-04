from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from main.models import *


# Home Page
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def index(request):
  return render(request, 'adminpanel/index.html')


# Admin Login
def admin_login(request):
    if request.method == 'GET':
        return render(request, 'adminpanel/login.html')

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and (user.is_superuser or user.is_staff):
            login(request, user)
            if request.GET:
                return redirect(request.GET['next'])
            return redirect('adminpanel')

        else:
            messages.error(request, 'No such account')
            return render(request, 'adminpanel/login.html')


# Admin Logout
def admin_logout(request):
    logout(request)
    return redirect('/')


# Admin Required
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):  
    def test_func(self):
        return self.request.user.is_superuser and self.request.user.is_staff


# Staff Required
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):  
    def test_func(self):
        return self.request.user.is_staff


# Tutorial Page
class Tutorials(AdminRequiredMixin, StaffRequiredMixin, View):

    def get(self, request):
        all_tutorial = Tutorial.objects.all()
        all_root = RootTutorial.objects.all()
        all_catagories = CatagoryTutorial.objects.all()

        context = {
            'roots' : all_root,
            'catagories' : all_catagories,
            'tutorials': all_tutorial,
        }
        return render(request, 'adminpanel/tutorials.html', context)


    def post(self, request):    
        if request.POST["action"] == "create-root":           
            root_data = self.createRoot(request)
            return JsonResponse(root_data,safe=False)

        elif request.POST["action"] == "edit-root":
            root_data = self.editRoot(request)
            return JsonResponse(root_data,safe=False)

        elif request.POST["action"] == "delete-root":
            root_data = self.deleteRoot(request)
            return JsonResponse(root_data,safe=False)

        elif request.POST["action"] == "approve-root":
            root_data = self.approveRoot(request)
            return JsonResponse(root_data,safe=False)

        elif request.POST["action"] == "create-catagory":           
            catagory_data = self.createCatagory(request)
            return JsonResponse(catagory_data,safe=False)

    # Root Functioanlity
    def createRoot(self, request):
        rootName = request.POST["rootName"]

        try:
            root = RootTutorial(title=rootName)
            root.save()
            root_data={'id':root.id,'rootName':root.title,"error":False,"errorMessage":"Root Added Successfully!"}
            return root_data
        except:
            root_data={"error":True,"errorMessage":"Failed to Add Root!"}
            return root_data

    def editRoot(self, request):
        id = request.POST["id"]
        rootName = request.POST["rootName"]

        try:
            root = RootTutorial.objects.get(id=id)
            root.title = rootName
            root.save()

            root_data={'id':root.id,'rootName':root.title,"error":False,"errorMessage":"Root Updated Successfully!"}
            return root_data
        except:
            root_data={"error":True,"errorMessage":"Failed to Update Root!"}
            return root_data

    def deleteRoot(self, request):
        id = request.POST["id"]
        try:
            root = RootTutorial.objects.get(id=id)
            root.delete()
            root_data={"error":False,"errorMessage":"Root Deleted Successfully!"}
            return root_data
        except:
            root_data={"error":True,"errorMessage":"Failed to Delete Root!"}
            return root_data

    # Catagory Functioanlity
    def createCatagory(self, request):
        rootID = request.POST["rootID"]
        catagoryName = request.POST["catagoryName"]

        try:
            catagory = CatagoryTutorial( title = catagoryName, root_tutorial_id = rootID)
            catagory.save()
            catagory_data={'id':catagory.id,'catagoryName':catagory.title,'rootID':catagory.root_tutorial_id,"error":False,"errorMessage":"Catagory Added Successfully!"}
            return catagory_data
        except:
            root_data={"error":True,"errorMessage":"Catagory to Add Root!"}
            return root_data




"""
    def createTutorial(self, request):
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        userName = request.POST["userName"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.create_user(first_name=firstName, last_name=lastName, username=userName, email=email, password=password)
            user_data={'id':user.id,'firstName':user.first_name,'lastName':user.last_name,'userName':user.username,'email':user.email,'last_login':user.last_login,"error":False,"errorMessage":"User Added Successfully!"}
            return user_data
        except:
            user_data={"error":True,"errorMessage":"Failed to Add User!"}
            return user_data

    def editTutorial(self, request):
        id = request.POST["id"]
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        userName = request.POST["userName"]
        email = request.POST["email"]
        userRole = request.POST["userRole"]

        try:
            user=User.objects.get(id=id)
            user.first_name = firstName
            user.last_name = lastName
            user.username = userName
            user.email = email

            if userRole == "member":
                user.is_staff = False
                user.is_superuser = False
            elif userRole == "staff":
                user.is_staff = True
                user.is_superuser = False
            elif userRole == "admin":
                user.is_staff = True
                user.is_superuser = True 

            user.save()

            user_data={'id':user.id,'firstName':user.first_name,'lastName':user.last_name,'userName':user.username,'email':user.email,'last_login':user.last_login,"error":False,"errorMessage":"User Updated Successfully!"}
            return user_data
        except:
            user_data={"error":True,"errorMessage":"Failed to Update User!"}
            return user_data

    def deleteTutorial(self, request):
        id = request.POST["id"]
        try:
            user=User.objects.get(id=id)
            user.delete()
            user_data={"error":False,"errorMessage":"User Deleted Successfully!"}
            return user_data
        except:
            user_data={"error":True,"errorMessage":"Failed to Delete User!"}
            return user_data

    def approveTutorial(self,request):
        id = request.POST["id"]
        try:
            user = User.objects.get(id=id)
            account_activation_token = AccountActivationTokenGenerator()
            context = {
                'user': user,
                'domain': get_current_site(request).domain,
                'token': urlsafe_base64_encode(force_bytes(user.id)) + '.' + account_activation_token.make_token(user)
            }

            subject = 'Please confirm your email'
            body = render_to_string('adminpanel/email-verification.html', context)
            sender = 'noreply@hacksprint.me'
            receiver = [user.email]

            send_mail(subject, 'this is body', sender, receiver, fail_silently=False, html_message=body)

            user_data={"error":False,"errorMessage":"User Approval Email Sent Successfully!"}
            return user_data
        except:
            user_data={"error":True,"errorMessage":"Failed to sent Approval Email to User!"}
            return user_data
"""