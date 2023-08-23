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
from .models import ReportedBlogPost,ReportedComments,Suggestion,User
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from accounts.Forums import SignupForm
from django.contrib.auth.hashers import make_password
from accounts.mixins import RegularUserLoginRequiredMixin,ModeratorLoginRequiredMixin,AdminLoginRequiredMixin

class home_page(RegularUserLoginRequiredMixin,View): 
  
    # LOGIN_URL = 'accounts.views.user_login'    
    def get(self,request):
         blogs = BlogPost.objects.all().filter(is_apprroved=True)   # Retrieve the list of Person objects
         paginator = Paginator(blogs, 4)  # Show 4 persons per page
         page = request.GET.get('page')
         persons_page = paginator.get_page(page)
         
         
         return render(request,'Homepage.html',{'blogs_page': persons_page})
    def post(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url) 
   
class create_Blog(RegularUserLoginRequiredMixin,View):        
    def get(self,request):

         return render(request,'create_blog_form.html')
    def post(self,request):
     try:
       user = request.user
       print("User : ",user)
       if not request.FILES.get('blog_title_image'):     
            url = reverse('blog_home:writeblog')
            messages.error(request,"Image field is Required")
            return redirect(url)
       blog_title = request.POST.get('blogTitle')
       blog_content = request.POST.get('hiddenContent')
       description=request.POST['description']
       Category=request.POST['Category']
       blog_title_image=request.FILES['blog_title_image']                                
       new_blog = BlogPost(title=blog_title, content=blog_content, user=user,description=description,Category=Category,blog_title_image=blog_title_image)
       new_blog.save()
       messages.success(request,"Blog Send for Approval")
     except Exception as e:

       messages.error(request, f'An error occurred: {e}')
     url = reverse('blog_home:writeblog')
     return redirect(url) 
class view_list_Blog(RegularUserLoginRequiredMixin,View):             
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url) 
    def post(self,request):
       id=request.POST["blog_id"]
       
       url = reverse('blog_home:retrieveblog',args=[id])
    #    url_with_param = f"{url}?id={id}"
       return redirect(url) 

class view_retrieve_Blog(RegularUserLoginRequiredMixin,View):        
    def get(self,request,id):
       try:  
         blog_post = BlogPost.objects.filter(id=id).first() 
         print("I am here")  
         print(blog_post.title)
         
         comments=Comments.objects.all().filter(post__id=blog_post.id)
         print(comments)
         suggestions=Suggestion.objects.all().filter(post__id=blog_post.id)
         if suggestions.all().filter(user__id=request.user.id):
             hassuggestion= True
         else:
               hassuggestion= False
       except Exception as e:
           messages.error(request, f'An error occurred: {e}')          
       return render(request,'retrieve_blog.html',{'blog_post': blog_post,'all_comments':comments,'all_suggestions':suggestions,'hassuggestion':hassuggestion})
    def post(self,request,id):
       blog_post = BlogPost.objects.filter(id=id).first() 
       user=request.user
       text=request.POST["text"]
       attachment=None
       if request.POST["parent"]=="normal comment":
            if request.FILES.get("attachment"):
             attachment=request.FILES["attachment"]
            print(text)
    #    new_comment = Comments(text=text, name=user.name,email_address=user.email_address,parent=None)
            try:
                new_comment = Comments.objects.create(
                text=text,
                user=user,
                post=blog_post,
                parent=None,
                attachment=attachment
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

       url = reverse('blog_home:retrieveblog',args=[id])
       return redirect(url)

class add_comment(RegularUserLoginRequiredMixin,View):        
    def get(self,request,id):
         blog_post = BlogPost.objects.filter(id=id).first() 
         print("I am here")  
         print(blog_post.title)
         return render(request,'retrieve_blog.html',{'blog_post': blog_post})
    def post(self,request):
       id=request.POST["blog_id"]
       blog_post = BlogPost.objects.filter(id=id).first() 
       user=request.user
       text=request.POST["text"]
       
       
       parent_comment_id= request.POST["parent"]
       print("parent_comment_id",parent_comment_id)
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
       all_comments=Comments.objects.all().filter(post__id=blog_post.id,is_reply=True)
       all_comments=all_comments.filter(parent__id=parent_comment_id)
       
       updated_replies_html = render_to_string('replies-form-comment.html', {
            'all_comments': all_comments,'commentid':parent_comment_id,'blog_id':id,"session_user":user # Pass any necessary context
        })
        
        # You can also return the updated comment count if needed
       updated_comment_count = all_comments.count()
    #    print(updated_replies_html)
        # Return the updated content as JSON response
       return JsonResponse({
            'updated_replies_html': updated_replies_html,
            'updat_comment_count': updated_comment_count
        })




class Profile(RegularUserLoginRequiredMixin,View):        
    def get(self,request):
        try: 
         user=request.user
         print(user)

         blogs = BlogPost.objects.all().filter(user__id=user.id)  # Retrieve the list of Person objects
         paginator = Paginator(blogs, 2)  # Show 4 persons per page
         blog_page = request.GET.get('page')
         post_page = paginator.get_page(blog_page)
        except Exception as e:
               messages.error(request, f'An error occurred: {e}')          
        return render(request,'profile.html',{'person': user,'post_page':post_page,'all_posts':blogs})
    def post(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)

class editProfile(RegularUserLoginRequiredMixin,View):        
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
        new_email=request.POST['email_address']
        print(request.user)
        try:  
            user=User.objects.get(pk=request.user.id)
            
            print(user)
            if not request.FILES.get("profile_pic"):
                request.FILES["profile_pic"]=user.profile_pic    
            
            user.email_address=request.POST["email_address"]
        
            user.name=request.POST["name"]
            user.age=request.POST["age"]
            user.profile_pic=request.FILES["profile_pic"]
            user.password=make_password(request.POST["password"])
            print(user)
            user.save()
            login(request,user)
            messages.success(request, 'Account updated successfully')
        except Exception as e:
               messages.error(request, f'An error occurred: {e}')         
        url = reverse('blog_home:profile')
        return redirect(url)

class ReportComment(RegularUserLoginRequiredMixin,View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)            
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
     id=request.POST["blog_id"]
     print("Blog id is : ",id)
     try:  
       comment_id=request.POST["comment_id"]
       print("Comment id: ",comment_id)
       mesg=request.POST["message"]
       user=request.user
       comment = Comments.objects.filter(id=comment_id).first()
       
       comment_exists = ReportedComments.objects.all().filter(comment__id=comment.id)
    #    reported_comments = ReportedComments.objects.filter(comment=comment)
       print("if it existss : ",comment_exists)
       if comment_exists:
            # Get the post that is being reported
            

            # Check if the user already reported this post
            user_already_reported = ReportedComments.objects.filter(comment__id=comment_id).first()
            # print(user_already_reported.user.all())
            if user not in user_already_reported.user.all():
                # Create a new ReportPost entry and associate it with the user
                report = ReportedComments.objects.filter(comment__id=comment.id).first()
                report.user.add(user)
                report.save()
                messages.success(request, 'Reported Succesfullyy')
            else:
                    #    print("I am in report comment")
                       messages.error(request, 'Already Reported this comment')
                      
       else:
        report =ReportedComments.objects.create(message=mesg,comment=comment)
        report.user.add(user)
        report.save()
        messages.success(request, 'Reported Succesfully')
     except Exception as e:
               messages.error(request, f'An error occurred: {e}')         
     url = reverse('blog_home:retrieveblog',args=[id])
     return redirect(url)  
class LikeComment(RegularUserLoginRequiredMixin,View):  
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)          
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
      try:  
       user=request.user
    #    id=request.POST["blog_id"]
       comment_id=request.POST["comment_id"]
       blog_post = Comments.objects.filter(id=comment_id).first()
       
       if user not in blog_post.isLiked.all():
             blog_post.isLiked.add(user)
             
             isliked=0
             print("user added")
       elif user in blog_post.isLiked.all():     
             blog_post.isLiked.remove(user)
             isliked=1
             print("user removed")
       likes_count = blog_post.isLiked.count()
       print(blog_post.isLiked.all())
      except Exception as e:
            #    print("exception occured")
               messages.error(request, f'An error occurred: {e}')     
       
      return JsonResponse({'likes': likes_count,'isliked':isliked}) 
   
class ReportPost(RegularUserLoginRequiredMixin,View):        
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
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

            if user_already_reported:
                # Create a new ReportPost entry and associate it with the user
                report = ReportedBlogPost.objects.filter(post=blog_post).first()
                report.message=report.message+","+mesg
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
class LikePost(RegularUserLoginRequiredMixin,View):        
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       blog_post = BlogPost.objects.filter(id=id).first()
       print("we are in here")
       if user not in blog_post.isLiked.all():
             blog_post.isLiked.add(user)
             
             isliked=0
       elif user in blog_post.isLiked.all():     
             blog_post.isLiked.remove(user)
             isliked=1
       likes_count = blog_post.isLiked.count()
       print(blog_post.isLiked.all())
       print("we are here now in view")
       return JsonResponse({'likes': likes_count,'isliked':isliked}) 

class AddSuggestion(RegularUserLoginRequiredMixin,View):        
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       text=request.POST["text"]
       blog_post = BlogPost.objects.filter(id=id).first()
       new_suggestion = Suggestion.objects.create(
                text=text,
                user=user,
                post=blog_post,
                parent=None
                )
       print("user : ",user)

       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url)   
class RetrieveSuggestion(RegularUserLoginRequiredMixin,View):        
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       blog_post = BlogPost.objects.filter(id=id).first()
       if user not in blog_post.isLiked.all():
             blog_post.isLiked.add(user)
       
       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url)

class UpdateYourSuggestion(RegularUserLoginRequiredMixin,View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)           
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
    #    user=request.user
       id=request.POST["suggestion_id"]
       text = request.POST.get('text')
       print(text)
       print("in update suggetsion")
       try:
            suggestion = Suggestion.objects.get(pk=id)
            suggestion.text = text
            suggestion.save()
            
            # Prepare the response data
            response_data = {
                "status": "success",
                "message": "Suggestion updated successfully",
                "updated_text": text,
            }
            
       except Suggestion.DoesNotExist:
            response_data = {
                "status": "error",
                "message": "Suggestion not found",
            }
       

       return JsonResponse(response_data)      
class ListSuggestion(RegularUserLoginRequiredMixin,View):
      
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       blog_post = BlogPost.objects.filter(id=id).first()
       if user not in blog_post.isLiked.all():
             blog_post.isLiked.add(user)
       
       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url)
class disLikeSuggestion(RegularUserLoginRequiredMixin,View):        
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       suggestion_id=request.POST["suggestion_id"]
       blog_post = Suggestion.objects.filter(id=suggestion_id).first()
       if user  in blog_post.isLiked.all():
             blog_post.isLiked.remove(user)
       
       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url) 
class LikeSuggestion(RegularUserLoginRequiredMixin,View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)        
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       suggestion_id=request.POST["suggestion_id"]
       blog_post = Suggestion.objects.filter(id=suggestion_id).first()
       
       if user not in blog_post.isLiked.all():
             blog_post.isLiked.add(user)
             
             isliked=0
       elif user in blog_post.isLiked.all():     
             blog_post.isLiked.remove(user)
             isliked=1
       likes_count = blog_post.isLiked.count()
       print(blog_post.isLiked.all())
       print("we are here now in view")
       return JsonResponse({'likes': likes_count,'isliked':isliked})  




class RejectSuggestion(RegularUserLoginRequiredMixin,View):        
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
    #    user=request.user
       suggestion_id=request.POST["suggestion_id"]
       id=request.POST["blog_id"]
       blog_post = Suggestion.objects.get(id=suggestion_id).delete()
       
       url = reverse('blog_home:retrieveblog',args=[id]) 
       return redirect(url)
    




class ReplySuggestion(RegularUserLoginRequiredMixin,View):        
    def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)
    def post(self,request):
       user=request.user
       id=request.POST["blog_id"]
       text=request.POST["text"]
       suggestion_id=request.POST["parent"]
       print("Parent is this here : ",suggestion_id)
       suggestion = Suggestion.objects.filter(id=suggestion_id).first()
       blog_post = BlogPost.objects.filter(id=id).first()
       new_suggestion = Suggestion.objects.create(
                text=text,
                user=user,
                post=blog_post,
                parent=suggestion,
                is_reply=True
                )
      
       all_suggestions=Suggestion.objects.all().filter(post__id=blog_post.id,is_reply=True)
       all_suggestions=all_suggestions.filter(parent__id=suggestion_id)
       
       updated_replies_html = render_to_string('replies-form-suggest.html', {
            'all_suggestions': all_suggestions,'blog_id':id,"session_user":user# Pass any necessary context
        })
       print(updated_replies_html)
        # You can also return the updated comment count if needed
       updated_comment_count = all_suggestions.count()
    #    print(updated_replies_html)
        # Return the updated content as JSON response
       return JsonResponse({
            'updated_replies_html': updated_replies_html,
            'updated_comment_count': updated_comment_count
        })
      

import cloudinary
          
import cloudinary
          
cloudinary.config( 
  cloud_name = "dhxwjjsjj", 
  api_key = "412286443281952", 
  api_secret = "wFL4hGHiEET8HbvrGenD_a0szUA" 
)
import cloudinary.uploader

class UploadImage(RegularUserLoginRequiredMixin,View):
   @method_decorator(csrf_exempt)
   def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
   def get(self,request):
     url = reverse('blog_home:homepage')
     return redirect(url)  
   def post(self,request):
        image_file = request.FILES.get('image')
        if image_file:
            # print(image_file)
            result = cloudinary.uploader.upload(image_file)
            image_url = result['secure_url']
            print(image_url)
            return JsonResponse({'url': image_url})
        messages.error(request,"Attachment image in Text editor not write")
        return JsonResponse({'error': 'Image upload failed.'})