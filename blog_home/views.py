from django.shortcuts import render
from blog_home import views
from django.views import View 
from .Forum import BlogForm
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.contrib.auth import authenticate ,login,logout
from .models import BlogPost
from .models import Comments
from .models import ReportedBlogPost,ReportedComments,Suggestion
from django.core.paginator import Paginator
from django.contrib import messages
class home_page(View):        
    def get(self,request):
         blogs = BlogPost.objects.all()   # Retrieve the list of Person objects
         paginator = Paginator(blogs, 4)  # Show 4 persons per page
         page = request.GET.get('page')
         persons_page = paginator.get_page(page)
         
         
         return render(request,'Homepage.html',{'blogs_page': persons_page})
    def post(self,request):
       pass 
class create_Blog(View):        
    def get(self,request):

         return render(request,'create_blog_form.html')
    def post(self,request):
       user = request.user
       print("User : ",user)
       blog_title = request.POST.get('blogTitle')
       blog_content = request.POST.get('hiddenContent')
       description=request.POST['description']
       Category=request.POST['Category']
       print(request.POST)
       print(request.FILES)
       blog_title_image=request.FILES['blog_title_image']                                
       print("blog_content : ",blog_content)
       new_blog = BlogPost(title=blog_title, content=blog_content, user=user,description=description,Category=Category,blog_title_image=blog_title_image)
       new_blog.save()
       return HttpResponse('Success')
class view_list_Blog(View):        
    def get(self,request):
         blog_posts = BlogPost.objects.all()   
         return render(request,'list_blogs.html',{'blog_posts': blog_posts})
    def post(self,request):
       id=request.POST["blog_id"]
       
       url = reverse('blog_home:retrieveblog',args=[id])
    #    url_with_param = f"{url}?id={id}"
       return redirect(url) 

class view_retrieve_Blog(View):        
    def get(self,request,id):
         blog_post = BlogPost.objects.filter(id=id).first() 
         print("I am here")  
         print(blog_post.title)
         comments=Comments.objects.all()
         return render(request,'retrieve_blog.html',{'blog_post': blog_post,'all_comments':comments})
    def post(self,request,id):
       blog_post = BlogPost.objects.filter(id=id).first() 
       user=request.user
       text=request.POST["text"]
       if request.POST["parent"]=="normal comment":
            print(text)
    #    new_comment = Comments(text=text, name=user.name,email_address=user.email_address,parent=None)
            try:
                new_comment = Comments.objects.create(
                text=text,
                user=user,
                post=blog_post,
                parent=None
                )
        # Comment instance created successfully
            except Exception as e:
        # Handle any errors that occurred during comment creation
        # You can print the error or log it for debugging
               print(f"Error creating comment: {e}")
            print(new_comment)
            new_comment.save()
       else:
           parent_comment_id= request.POST["parent"]
           parent=Comments.objects.all().get(id=parent_comment_id)
           try:
                new_comment = Comments.objects.create(
                text=text,
                user=user,
                parent=parent,
                post=blog_post,
                is_reply=True
                )
        # Comment instance created successfully
           except Exception as e:
               print(f"Error creating comment: {e}")

       comments=Comments.objects.all()
       return render(request,'retrieve_blog.html',{'blog_post': blog_post,'all_comments':comments})

class add_comment(View):        
    def get(self,request,id):
         blog_post = BlogPost.objects.filter(id=id).first() 
         print("I am here")  
         print(blog_post.title)
         return render(request,'retrieve_blog.html',{'blog_post': blog_post})
    def post(self,request):
       id=request.POST["blog_id"]
       print(id)
       
       url = reverse('blog_home:retrieveblog')
       url_with_param = f"{url}?id={id}"
       return redirect(url)

class Profile(View):        
    def get(self,request):
         user=request.user
         print(user)
         return render(request,'profile.html',{'user': user})
    def post(self,request):
       url = reverse('blog_home:editprofile')
       return redirect(url) 

class editProfile(View):        
    def get(self,request):
         user=request.user
         print(user)
         return render(request,'editprofile.html',{'user': user})
    def post(self,request):
       id=request.POST["blog_id"]
       print(id)
       
       url = reverse('blog_home:retrieveblog',args=[id])
       return redirect(url)

class ReportComment(View):        
    def get(self,request):
        pass
    def post(self,request):
       id=request.POST["comment_id"]
       mesg=request.POST["message"]
       user=request.user
       comment = Comments.objects.filter(id=id).first()
       print(id)
       post_exists = ReportedComments.objects.filter(comment=comment).exists()
       print("I am in report comment")
       if post_exists:
            # Get the post that is being reported
            

            # Check if the user already reported this post
            user_already_reported = user.reported_comments.filter(id=comment.id).exists()

            if not user_already_reported:
                # Create a new ReportPost entry and associate it with the user
                report = ReportedComments.objects.filter(id=comment.id).first()
                report.user.add(user)
                report.save()
                messages.success(request, 'Reported Succesfully')
            else:
                       messages.error(request, 'Already Reported this comment')
                      
       else:
        report =ReportedComments.objects.create(message=mesg,comment=comment)
        report.user.add(user)
        report.save()
        messages.success(request, 'Reported Succesfully')
       url = reverse('blog_home:retrieveblog',args=[id])
       return redirect(url)  
class LikeComment(View):        
    def get(self,request):
         pass
    def post(self,request):
       user=request.user
       id=request.POST["comment_id"]
       comments = Comments.objects.filter(id=id).first()
       if user not in comments.isLiked.all():
             comments.isLiked.add(user)
       url = reverse('blog_home:retrieveblog',args=[id])      
       return redirect(url) 
class ReportPost(View):        
    def get(self,request):
               pass
    def post(self,request):
       id=request.POST["blog_id"]
       mesg=request.POST["message"]
       user=request.user
       blog_post = BlogPost.objects.filter(id=id).first()
       post_exists = ReportedBlogPost.objects.filter(post=blog_post).exists()

       if post_exists:
            # Get the post that is being reported
            

            # Check if the user already reported this post
            user_already_reported = user.reported_posts.filter(id=blog_post.id).exists()

            if not user_already_reported:
                # Create a new ReportPost entry and associate it with the user
                report = ReportedBlogPost.objects.filter(post=blog_post).first()
                report.user.add(user)
                report.save()
                messages.success(request, 'Reported Succesfully')
            else:
                       messages.error(request, 'Already Reported this Post')
       else:
        report =ReportedBlogPost.objects.create(message=mesg,post=blog_post)
        report.user.add(user)
        report.save()
        messages.success(request, 'Reported Succesfully')
                # post.reported_posts.add(report)
            # Entry already exists, handle as needed
            
    #    print(id)
       
       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url)    
class LikePost(View):        
    def get(self,request):
        pass
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       blog_post = BlogPost.objects.filter(id=id).first()
       if user not in blog_post.isLiked.all():
             blog_post.isLiked.add(user)
       
       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url)  

class AddSuggestion(View):        
    def get(self,request):
        pass
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       new_comment = Comments.objects.create(
                text=text,
                user=user,
                post=blog_post,
                parent=None
                )
       blog_post = BlogPost.objects.filter(id=id).first()
       if user not in blog_post.isLiked.all():
             blog_post.isLiked.add(user)
       
       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url)   
class RetrieveSuggestion(View):        
    def get(self,request):
        pass
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       blog_post = BlogPost.objects.filter(id=id).first()
       if user not in blog_post.isLiked.all():
             blog_post.isLiked.add(user)
       
       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url) 
class ListSuggestion(View):        
    def get(self,request):
        pass
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       blog_post = BlogPost.objects.filter(id=id).first()
       if user not in blog_post.isLiked.all():
             blog_post.isLiked.add(user)
       
       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url)       



