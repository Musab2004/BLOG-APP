from django.shortcuts import render
from django.views import View 
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.contrib.auth import authenticate ,login,logout
from .Forums import SignupForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from .models import User
# Create your views here.
from axes.signals import user_locked_out
from django.dispatch import receiver

@receiver(user_locked_out)
class Login(View):
    def get(self,request):
         login_attempt=0        
         
         return render(request,'auth_forms.html',{'login_attempts':login_attempt, 'islogin':1})
    def post(self,request):
    #  print(r
        print("In Login")
        email_address=request.POST["email_address"]
        password=request.POST["password"]
        
        print(email_address)
  
        user = authenticate(request, email_address=email_address, password=password)
        
        if user is not None:
            # User is valid, log them in
            login(request, user)
            if user.is_staff==True:
             print("here in login")
             url = reverse('administrator:user')
             return redirect(url)
            elif user.is_moderator==True:
             url = reverse('administrator:unpublish_post')
             return redirect(url)

            else:
             print("here in login")    
             url = reverse('blog_home:homepage')
             return redirect(url)
        else:
    
 
            messages.error(request,"invalid ccredentials") 
            return render(request,'auth_forms.html')
    
    # If the request method is not POST, render the login form

    

class Signup(View):        
    def get(self,request):
         
         return render(request,'auth_forms.html')
    def post(self,request):
        
        email_address=request.POST['email_address']
        # if User.objects.all().filter(email_address=email_address)
        try:
            form = SignupForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created successfully')
            else:
                error_messages = "\n".join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
                messages.error(request, f'Form validation failed:\n{error_messages}')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}') 
    # If the request method is not POST, render the login form
        
        return render(request,'auth_forms.html',)

class Logout(View):        
    def get(self,request):
        logout(request)
        url=reverse('user_login')
        return redirect(url)
        
    # def post(self,request):
    #     logout(request)
    #     url=reverse('regist')
    #     return redirect(url)

        