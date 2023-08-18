from django.shortcuts import render
from django.views import View 
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.contrib.auth import authenticate ,login,logout
from .Forums import SignupForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# Create your views here.
class Login(View):        
    def get(self,request):
         
         return render(request,'auth_forms.html')
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
            url = reverse('blog_home:homepage')
            return redirect(url)
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request,'auth_forms.html')
    
    # If the request method is not POST, render the login form
        return render(request, "Login_form.html")
    

class Signup(View):        
    def get(self,request):
         
         return render(request,'auth_forms.html')
    def post(self,request):
        print("In Signup")
        print(request.FILES)
        form = SignupForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
          form.save()
          messages.success(request, 'Account created Succesfully')
          return render(request,'auth_forms.html') 
    # If the request method is not POST, render the login form
        
        return HttpResponse("Failed")   


        