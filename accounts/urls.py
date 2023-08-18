from django.contrib import admin
from django.urls import path
from django.urls import include
from accounts import views
from django.views.generic import TemplateView

  

urlpatterns = [

    path('Signup',views.Signup.as_view(),name="user_signup"),
    path('regist', views.Login.as_view(),name="user_login"),
    # path('Home',views.Login.as_view(),name="user_home")
 
]
