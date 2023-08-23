from django.shortcuts import render


from django.views import View 
from accounts.mixins import RegularUserLoginRequiredMixin,ModeratorLoginRequiredMixin,AdminLoginRequiredMixin
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.contrib.auth import authenticate ,login,logout

from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import User
from blog_home.models import BlogPost,ReportedBlogPost,ReportedComments,Comments,Suggestion
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.Forums import SignupForm
# Create your views here.
class HomePage(AdminLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request,tab_name):

        #  for report in reports:
        #   print(report.post)


         




         
         return render(request,'Homepage_admin.html',{})
    def post(self,request):
       pass

class HomePageModerator(ModeratorLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request,tab_name):
         blogs = BlogPost.objects.all().filter(is_apprroved=False)   # Retrieve the list of Person objects
         paginator = Paginator(blogs, 4)  # Show 4 persons per page
         blog_page = request.GET.get('page')
         post_page = paginator.get_page(blog_page)
         

         reports=ReportedBlogPost.objects.all()
         paginator = Paginator(reports, 4)  # Show 4 persons per page
         report_page = request.GET.get('page')
         report_post_page = paginator.get_page(report_page)
         for post in report_post_page:
           print(post.message)

         return render(request,'Moderator_Homepage.html',{'post_page': post_page,'report_post_page':report_post_page,'tab_name':tab_name})
    def post(self,request):
       pass 
class UserView(View):
    def get(self, request):
         users = User.objects.all().filter(is_staff=False ,is_moderator=False)   # Retrieve the list of Person objects
         paginator = Paginator(users, 4)  # Show 4 persons per page
         user_page = request.GET.get('page')
         persons_page = paginator.get_page(user_page)        
         return render(request, 'user.html',{'persons_page':persons_page})

class PostView(View):
    def get(self, request):
         blogs = BlogPost.objects.all().filter(is_apprroved=True)   # Retrieve the list of Person objects
         paginator = Paginator(blogs, 4)  # Show 4 persons per page
         blog_page = request.GET.get('page')
         post_page = paginator.get_page(blog_page)




         

         reports=ReportedBlogPost.objects.all()
         paginator = Paginator(reports, 4)  # Show 4 persons per page
         report_page = request.GET.get('report_page')
         report_post_page = paginator.get_page(report_page)
         all_posts=BlogPost.objects.all().filter(is_apprroved=True)
         all_users=User.objects.all().filter(is_staff=False,is_moderator=False)
         return render(request, 'posts.html',{'post_page': post_page, 'report_post_page':report_post_page,'all_posts':all_posts,
                                                      'all_users':all_users})

class SuggestionView(View):
    def get(self, request):
         reports=Suggestion.objects.all()
         paginator = Paginator(reports, 20)  # Show 4 persons per page
         suggest_page = request.GET.get('page')
         suggest_page = paginator.get_page(suggest_page)
         all_posts=BlogPost.objects.all().filter(is_apprroved=True)
         all_users=User.objects.all().filter(is_staff=False,is_moderator=False)
         return render(request, 'suggestions.html',{'suggest_page':suggest_page,'all_posts':all_posts,
                                                      'all_users':all_users})

class CommentView(View):
    def get(self, request):
         reports=ReportedComments.objects.all()
         paginator1 = Paginator(reports, 4)  # Show 4 persons per page
         report_page = request.GET.get('report_page')
         report_comment_page = paginator1.get_page(report_page)
        


         reports=Comments.objects.all()
         paginator = Paginator(reports, 20)  # Show 4 persons per page
         comment_page = request.GET.get('page')
         comment_page = paginator.get_page(comment_page)
         all_posts=BlogPost.objects.all().filter(is_apprroved=True)
         all_users=User.objects.all().filter(is_staff=False,is_moderator=False)
         return render(request, 'comments.html',{'report_comment_page':report_comment_page,
                                                      'comment_page':comment_page,'all_posts':all_posts,
                                                      'all_users':all_users})     

class UnpublishPostView(View):
    def get(self, request):
         reports=ReportedBlogPost.objects.all()
         paginator = Paginator(reports, 4)  # Show 4 persons per page
         report_page = request.GET.get('page')
         report_post_page = paginator.get_page(report_page)
         return render(request, 'unpublish_post.html',{'report_post_page':report_post_page})

class ApprovePostView(View):
    def get(self, request):
        # Logic to approve a post
         blogs = BlogPost.objects.all().filter(is_apprroved=False)   # Retrieve the list of Person objects
         paginator = Paginator(blogs, 4)  # Show 4 persons per page
         blog_page = request.GET.get('page')
         post_page = paginator.get_page(blog_page)        
         return render(request, 'approve_post.html',{'post_page': post_page})
class CreateUser(AdminLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request):
        pass
    def post(self,request):
        form = SignupForm(request.POST,request.FILES)
        print("in Created")
        if form.is_valid():
          form.save()
          messages.success(request, 'Account created Succesfully')
        else:

            error_messages = "\n".join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
            messages.error(request, f'Form validation failed:\n{error_messages}')
        tab_name="user"
        
        url = reverse('administrator:user') 
        return redirect(url)

class UpdateUser(AdminLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request):
        pass
    def post(self,request,id):
        new_email=request.POST['email_address']
        user=User.objects.get(pk=id)
        if User.objects.all().filter(email_address=new_email).exists():
                print("already exixts")
                return render(request, 'update_profile.html', {'error': 'Email address already exists.'})
        
        user.email_address=request.POST["email_address"]
       
        user.name=request.POST["name"]
        user.age=request.POST["age"]
        if request.FILES.get("profile_pic"):
           user.profile_pic=request.FILES["profile_pic"]
        user.save()
        form = SignupForm(request.POST,request.FILES)
        messages.success(request, 'Account updated Succesfully')
        tab_name="user"
        
        url = reverse('administrator:user') 
        return redirect(url)         
class DeleteUser(AdminLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request):
        pass
    def post(self,request,id):
     try:
        user=User.objects.get(pk=id)
        user.delete()
        # if form.is_valid():
        #   form.save()
        messages.success(request, 'Deletion Succesfull')

       
     except Exception as e:

       messages.error(request, f'An error occurred: {e}')
     tab_name="user"
        
     url = reverse('administrator:user') 
     return redirect(url) 



class CreatePost(AdminLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request):
        pass
    def post(self,request):
    #    user = request.user
    #    print("User : ",user)
     try:
       blog_title = request.POST.get('blogTitle')
       blog_content = request.POST.get('hiddenContent')
       description=request.POST['description']
       Category=request.POST['Category']
    #    if request.FILES.get('blog_title_image'):
       blog_title_image=request.FILES['blog_title_image']
    #    else:
            
       selected_user_id = request.POST.get('user_choice')
       
    
       if selected_user_id:
        user = User.objects.get(id=selected_user_id)                                
       new_blog = BlogPost(title=blog_title, content=blog_content, user=user,description=description,Category=Category,blog_title_image=blog_title_image,is_apprrovd=True)
       new_blog.save()
       messages.success(request, 'Account created Succesfully') 
       
     except Exception as e:

       messages.error(request, f'An error occurred: {e}')
     tab_name="post"  
     url = reverse('administrator:posts') 
     return redirect(url)

class UpdatePost(AdminLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request):
        pass
    def post(self,request,id):
       
       post=BlogPost.objects.get(pk=id)
       post.title = request.POST.get('blogTitle')
    #    post.blog_content = request.POST.get('hiddenContent')
       post.description=request.POST['description']
       post.Category=request.POST['Category']
       if request.FILES.get('blog_title_image'):
        post.blog_title_image=request.FILES['blog_title_image']

    #    selected_user_id = request.POST.get('user_choice')
    #    if selected_user_id:
    #     user = User.objects.get(id=selected_user_id)
    #     post.user=user
       post.save() 

        
       url = reverse('administrator:posts') 
       return redirect(url)


class ApprovePost(ModeratorLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request):
        pass
    def post(self,request,id):
       try:
        post=BlogPost.objects.get(pk=id)
        post.is_apprroved= True
        post.save()
       except:
           messages.error(request,'Error in getting Blog post')
    #    tab_name="approve" 

       url = reverse('administrator:approve_post') 
       return redirect(url)    
class DeletePost(AdminLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request):
        pass
    def post(self,request,id):
       try: 
        blog=BlogPost.objects.get(pk=id)
        blog.delete()
        # if form.is_valid():
        #   form.save()
        messages.success(request, 'Deletion Succesfull')
        tab_name="unpublish"
       except Exception as e:
            messages.error(request, f'An error occurred: {e}')  
       url = reverse('administrator:posts') 
       return redirect(url)
class DeletePostModerator(ModeratorLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request):
        pass
    def post(self,request,id):
       try: 
        blog=BlogPost.objects.get(pk=id)
        blog.delete()

        messages.success(request, 'Post Deleted Succesfull')
       except Exception as e:
            messages.error(request, f'An error occurred: {e}')   
       url = reverse('administrator:unpublish_post') 
       return redirect(url)    
class DeleteComment(AdminLoginRequiredMixin,View): 
 
    def get(self,request):
        pass
    def post(self,request,id):
       try: 
        comment=Comments.objects.get(pk=id)
        comment.delete()
        # if form.is_valid():
        #   form.save()
        messages.success(request, 'Deletion Succesfull')
       except Exception as e:
            messages.error(request, f'An error occurred: {e}')        

       url = reverse('administrator:comments') 
       return redirect(url)
class DeleteSuggestion(AdminLoginRequiredMixin,View): 
   
    def get(self,request):
        pass
    def post(self,request,id):
     try:
        comment=Suggestion.objects.get(pk=id)
        comment.delete()
        messages.success(request,"Suggestion deleted successfully")
     except Exception as e:
        messages.error(request,"An error occurred: {str(e)}")
     url = reverse('administrator:suggestions') 
     return redirect(url)     
class CreateSuggestion(View):        
    def get(self,request):
        pass
    def post(self,request):
      try: 
       id=request.POST["blog_id"]
       user_id=request.POST["user_id"]
       text=request.POST["text"]
       blog_post = BlogPost.objects.filter(id=id).first()
       user = User.objects.filter(id=user_id).first()
       new_suggestion = Suggestion.objects.create(
                text=text,
                user=user,
                post=blog_post,
                parent=None
       )
       messages.success(request,"Suggestion added successfully")
      except Exception as e:
        messages.error(request,f'An error occurred: {str(e)}')       

      url = reverse('administrator:suggestions') 
      return redirect(url)  
class CreateComment(View):        
    def get(self,request):
        pass
    def post(self,request):
      try:  
       id=request.POST["blog_id"]
       user_id=request.POST["user_id"]
       text=request.POST["text"]
       blog_post = BlogPost.objects.filter(id=id).first()
       user = User.objects.filter(id=user_id).first()
       new_suggestion = Comments.objects.create(
                text=text,
                user=user,
                post=blog_post,
                parent=None
                )
       messages.success(request,"Suggestion added successfully")
      except Exception as e:
        messages.error(request,"An error occurred: {str(e)}")         

      tab_name="comment"
      url = reverse('administrator:comments') 
      return redirect(url)