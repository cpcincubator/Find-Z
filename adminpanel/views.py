from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from main.models import *
from adminpanel.form import *


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
            messages.error(request, 'Invalid Credentials!')
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



# Home Page
class Index(AdminRequiredMixin and StaffRequiredMixin, View):
    def get(self, request):
        all_root = Root.objects.all().count()
        all_catagory = Catagory.objects.all().count()

        all_tutorial = Tutorial.objects.all().count()
        active_tutorial = Tutorial.objects.filter(is_active = '1').count()

        all_user = User.objects.all().count()
        active_user = User.objects.filter(is_active = '1').count()

        context = {
            'all_root': all_root,
            'all_catagory': all_catagory,
            'all_tutorial': all_tutorial,
            'active_tutorial': active_tutorial,
            'all_user': all_user,
            'active_user': active_user,
        } 
        return render(request, 'adminpanel/index.html', context)



# Catagory Page
class Catagories(AdminRequiredMixin and StaffRequiredMixin, View):
    def get(self, request):            
        all_root = Root.objects.all()
        all_catagory = Catagory.objects.all()

        context = {
            'roots' : all_root,
            'catagories' : all_catagory,
        }
        return render(request, 'adminpanel/catagories.html', context)


    def post(self, request):    
        if request.POST["action"] == "create-root":           
            root_data = self.createRoot(request)
            return JsonResponse(root_data, safe=False)

        elif request.POST["action"] == "edit-root":
            root_data = self.editRoot(request)
            return JsonResponse(root_data, safe=False)

        elif request.POST["action"] == "delete-root":
            root_data = self.deleteRoot(request)
            return JsonResponse(root_data, safe=False)


        elif request.POST["action"] == "create-catagory":           
            catagory_data = self.createCatagory(request)
            return JsonResponse(catagory_data, safe=False)

        elif request.POST["action"] == "edit-catagory":
            catagory_data = self.editCatagory(request)
            return JsonResponse(catagory_data, safe=False)

        elif request.POST["action"] == "delete-catagory":
            catagory_data = self.deleteCatagory(request)
            return JsonResponse(catagory_data, safe=False)


    # Root Functioanlity
    def createRoot(self, request):
        rootName = request.POST["rootName"]

        try:
            root = Root(title=rootName)
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
            root = Root.objects.get(id=id)
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
            root = Root.objects.get(id=id)
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
            catagory = Catagory( title = catagoryName, root_id = rootID)
            catagory.save()
            catagory_data = {'id':catagory.id,'catagoryName':catagory.title,'rootID':catagory.root_id,'rootName':catagory.root.title,'avatar':catagory.avatar,"error":False,"errorMessage":"Catagory Added Successfully!"}
            return catagory_data
        except:
            catagory_data = {"error":True,"errorMessage":"Failed to Add Catagory!"}
            return catagory_data

    def editCatagory(self, request):
        id = request.POST["id"]
        catagoryName = request.POST["catagoryName"]
        rootID = request.POST["rootID"]

        try:
            catagory = Catagory.objects.get(id=id)
            catagory.title = catagoryName
            catagory.root_id = rootID
            catagory.save()

            catagory_data = {'id':catagory.id,'catagoryName':catagory.title,'rootID':catagory.root_id,'rootName':catagory.root.title,'avatar':catagory.avatar,"error":False,"errorMessage":"Catagory Updated Successfully!"}
            return catagory_data
        except:
            catagory_data = {"error":True,"errorMessage":"Failed to Update Catagory!"}
            return catagory_data


    def deleteCatagory(self, request):
        id = request.POST["id"]
        try:
            catagory = Catagory.objects.get(id=id)
            catagory.delete()
            catagory_data = {"error":False,"errorMessage":"Catagory Deleted Successfully!"}
            return catagory_data
        except:
            catagory_data = {"error":True,"errorMessage":"Failed to Delete Catagory!"}
            return catagory_data




# Tutorial Page
class Tutorials(AdminRequiredMixin and StaffRequiredMixin, View):

    def get(self, request):
        if 'term' in request.GET:
            all_catagories = Catagory.objects.filter(title__icontains=request.GET.get('term'))
            titles = list()
            for catagory in all_catagories:
                titles.append(catagory.title)
            return JsonResponse(titles, safe=False)
            
        all_tutorial = Tutorial.objects.all()
        all_root = Root.objects.all()
        all_catagories = Catagory.objects.all()
        form = TutorialForm()

        context = {
            'roots' : all_root,
            'catagories' : all_catagories,
            'tutorials': all_tutorial,
            'form': form,
        }
        return render(request, 'adminpanel/tutorials.html', context)


    def post(self, request):    
        if request.POST["action"] == "create-tutorial":           
            tutorial_data = self.createTutorial(request)
            return JsonResponse(tutorial_data, safe=False)

        elif request.POST["action"] == "edit-tutorial":           
            tutorial_data = self.editTutorial(request)
            return JsonResponse(tutorial_data, safe=False)

        elif request.POST["action"] == "delete-tutorial":           
            tutorial_data = self.deleteTutorial(request)
            return JsonResponse(tutorial_data, safe=False)

    # Tutorial Functioanlity
    def createTutorial(self, request):
        catagoryName = request.POST["catagory"]
        tutorialName = request.POST["tutorialName"]
        tutorialURL = request.POST["tutorialURL"]
        tutorialDesc = request.POST["tutorialDesc"]

        try:
            catagory = Catagory.objects.get( title = catagoryName ) 
            catagoryID = catagory.id
            tutorial = Tutorial( title = tutorialName, desc = tutorialDesc, url = tutorialURL, catagory_id = catagoryID, is_active = True)
            tutorial.save()
            tutorial_data = {'id':tutorial.id,'tutorialName':tutorial.title,'catagoryName':tutorial.catagory.title,'rootName':tutorial.catagory.root.title,'tutorialURL':tutorial.url,'tutorialDesc':tutorial.desc,"error":False,"errorMessage":"Tutorial Added Successfully!"}
            return tutorial_data
        except:
            tutorial_data = {"error":True,"errorMessage":"Failed to Add Tutorial!"}
            return tutorial_data

    def deleteTutorial(self, request):
        id = request.POST["id"]
        try:
            tutorial = Tutorial.objects.get(id=id)
            tutorial.delete()
            tutorial_data = {"error":False,"errorMessage":"Tutorial Deleted Successfully!"}
            return tutorial_data
        except:
            tutorial_data = {"error":True,"errorMessage":"Failed to Delete Tutorial!"}
            return tutorial_data




# Users Page
class Users(AdminRequiredMixin, View):
  
    def get(self, request):
        all_user = User.objects.all().order_by('-date_joined')
        return render(request, 'adminpanel/users.html', {'users': all_user})

    def post(self, request):    
        if request.POST["action"] == "create-user":           
            user_data = self.createUser(request)
            return JsonResponse(user_data,safe=False)

        elif request.POST["action"] == "edit-user":
            user_data = self.editUser(request)
            return JsonResponse(user_data,safe=False)

        elif request.POST["action"] == "delete-user":
            user_data = self.deleteUser(request)
            return JsonResponse(user_data,safe=False)

        elif request.POST["action"] == "approve-user":
            user_data = self.approveUser(request)
            return JsonResponse(user_data,safe=False)

    def createUser(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            if User.objects.filter(username=username).exists():
                user_data={"error":True,"errorMessage":"Username already exists!"}
                return user_data

            elif User.objects.filter(email=email).exists():
                user_data={"error":True,"errorMessage":"Already have an account with this email!"}
                return user_data

            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user_data={'id':user.id,'username':user.username,'email':user.email,"error":False,"errorMessage":"User Added Successfully!"}
                return user_data
        except:
            user_data={"error":True,"errorMessage":"Failed to Add User!"}
            return user_data

    def editUser(self, request):
        id = request.POST["id"]
        username = request.POST["username"]
        email = request.POST["email"]
        userRole = request.POST["userRole"]

        try:
            user=User.objects.get(id=id)
            user.username = username
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

            user_data={'id':user.id,'username':user.username,'email':user.email,"error":False,"errorMessage":"User Updated Successfully!"}
            return user_data
        except:
            user_data={"error":True,"errorMessage":"Failed to Update User!"}
            return user_data

    def deleteUser(self, request):
        id = request.POST["id"]
        try:
            user=User.objects.get(id=id)
            user.delete()
            user_data={"error":False,"errorMessage":"User Deleted Successfully!"}
            return user_data
        except:
            user_data={"error":True,"errorMessage":"Failed to Delete User!"}
            return user_data

    def approveUser(self,request):
        id = request.POST["id"]
        try:
            user = User.objects.get(id=id)
            user.is_active = True
            user.save()
            user_data={"error":False,"errorMessage":"User Approved Successfully!"}
            return user_data
        except:
            user_data={"error":True,"errorMessage":"Failed to Approve to User!"}
            return user_data
