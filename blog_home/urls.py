from django.contrib import admin
from django.urls import path
from django.urls import include
from blog_home import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
app_name = 'blog_home'
urlpatterns = [
    path('homepage',views.home_page.as_view(),name="homepage"),
    path('writeblog',views.create_Blog.as_view(),name="writeblog"),
    path('listblog',views.view_list_Blog.as_view(),name="listblog"),
    path('retrieveblog/<int:id>/',views.view_retrieve_Blog.as_view(),name="retrieveblog"),
    path('profile',views.Profile.as_view(),name="profile"),
    path('editprofile',views.editProfile.as_view(),name="editprofile"),
    path('likecomment',views.LikeComment.as_view(),name="likecomment"),
    path('likepost',views.LikePost.as_view(),name="likepost"),
     path('reportcomment',views.ReportComment.as_view(),name="reportcomment"),
    path('reportpost',views.ReportPost.as_view(),name="reportpost"),
    # path('Signup/<int:year>/',views.Auther.as_view(),name="insert_auther_form"),
    # path('bookSignup',views.Auther.as_view(),name="insert_book")
]

