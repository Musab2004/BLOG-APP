from django.contrib import admin
from django.urls import path
from django.urls import include
from administrator import views
from django.views.generic import TemplateView

  
app_name = 'administrator'
urlpatterns = [



   path('deleteuser/<int:id>/',views.DeleteUser.as_view(),name="deleteuser"),
   path('createuser',views.CreateUser.as_view(),name="createuser"),
   path('updateuser/<int:id>/',views.UpdateUser.as_view(),name="updateuser"),
     path('deletepost/<int:id>/',views.DeletePost.as_view(),name="deletepost"),
      path('deletepostmoderator/<int:id>/',views.DeletePostModerator.as_view(),name="deletepostmoderator"),
   path('createpost',views.CreatePost.as_view(),name="createpost"),
   path('updatepost/<int:id>/',views.UpdatePost.as_view(),name="updatepost"),
   path('deletecomment/<int:id>/',views.DeleteComment.as_view(),name="deletecomment"),
   path('deletesuggestion/<int:id>/',views.DeleteSuggestion.as_view(),name="deletesuggestion"),
    path('createcomment',views.CreateComment.as_view(),name="createcomment"),
   path('createsuggestion',views.CreateSuggestion.as_view(),name="createsuggestion"),
   path('approvepost/<int:id>/',views.ApprovePost.as_view(),name="approvepost"),
    path('user/', views.UserView.as_view(), name='user'),
    path('posts/', views.PostView.as_view(), name='posts'),
    path('suggestions/', views.SuggestionView.as_view(), name='suggestions'),
    path('comments/', views.CommentView.as_view(), name='comments'),
      path('unpublish_post/', views.UnpublishPostView.as_view(), name='unpublish_post'),
    path('approve_post/', views.ApprovePostView.as_view(), name='approve_post'),
    # path('Home',views.Login.as_view(),name="user_home")
 
]
