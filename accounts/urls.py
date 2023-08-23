from django.contrib import admin
from django.urls import path
from django.urls import include
from accounts import views
from django.views.generic import TemplateView

  
# app_name = 'admin'
urlpatterns = [

    path('Signup',views.Signup.as_view(),name="user_signup"),
    path('regist', views.Login.as_view(),name="user_login"),
    path('logout', views.Logout.as_view(),name="user_logout"),
    # path('Home',views.Login.as_view(),name="user_home")
 
]
