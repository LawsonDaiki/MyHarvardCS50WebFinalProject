from django.http import HttpResponse
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect 
from django.http import JsonResponse
from .models import *
from .forms import *


def followingPosts(request):
  
    if request.method == 'GET': 
  
        # getting all the objects of Post that the user is following
        userFollows = Following.objects.get(follower=request.user)
        followedUsers = userFollows.followingUsers.all()
        
        users = []
        for u in followedUsers:
            users.append(u.id)

        posts = Post.objects.filter(user__in=users)
        posts = posts.order_by('-timestamp').all()
        return render(request, 'photogram/home.html', {'posts' : posts})


def allPosts(request):
  
    if request.method == 'GET': 
  
        # getting all the objects of Post
        posts = Post.objects.all()
        posts = posts.order_by('-timestamp')
        return render(request, 'photogram/home.html', {'posts' : posts})

  
def createPost(request): 
  
    if request.method == 'POST': 
        form = PostCreationForm(request.POST, request.FILES) 
  
        if form.is_valid():
            postForm = form.save(commit=False) # Keep the user out of the form and add it on save to 'is_valid()' work
            postForm.user = request.user
            form.save() 
            return redirect('allPosts') 
    else: 
        form = PostCreationForm() 
    return render(request, 'photogram/createpost.html', {'form' : form}) 


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.filter(username=username).first()
            profile = Profile(user=user)
            profile.save()
            following = Following(follower=user)
            following.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('allPosts')
    else:
        form = UserRegisterForm()
    return render(request, 'photogram/register.html', {'form': form})


@login_required
def profileEdit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = p_form.save(commit=False) # Keep the user out of the form and add it on save to 'is_valid()' work
            profile.user = request.user
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('allPosts')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'photogram/profileedit.html', context)


def profile(request, username):
    if User.objects.filter(username=username).exists():
        userProfile = User.objects.get(username=username)

        # Get profile following status
        followersCount = Following.objects.filter(followingUsers=userProfile.id).count()
        userFollows = Following.objects.get(follower=userProfile.id)
        followingCount = userFollows.followingUsers.all().count()
    
        posts_list = Post.objects.filter(user=userProfile.id)
        posts_list = posts_list.order_by('-timestamp').all()

        context = {
            'userProfile': userProfile,
            'posts': posts_list,
            'followers': followersCount,
            'following': followingCount,
        }
        return render(request, "photogram/profile.html", context)
    else:
        return HttpResponse("User not found. Sorry.")


def likePost(request, postid):

    # Update like request must be via PUT
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check if the post exists
    try:
        post = Post.objects.get(pk=postid)

        # Check if the 'like' already exists
        try:
            like = Likes.objects.get(user=request.user.id, post=postid)
            like.delete()

            # Update the post like count
            if post.likeCount > 0:
                post.likeCount = post.likeCount - 1
                print(post.likeCount)
                post.save()

            return JsonResponse({"message": "desliked"}, status=201)
            
        except Likes.DoesNotExist:
            like = Likes(user=request.user, post=post)
            like.save()

            # Update the post like count
            post.likeCount = post.likeCount + 1
            print(post.likeCount)
            post.save()

            return JsonResponse({"message": "liked"}, status=201)

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)


def follow(request, username):

    if request.method == "GET":
        userToFollow = User.objects.get(username=username) # Get User to follow
        userFollowingData = Following.objects.get(follower=request.user) # Get Following object from the current logged user

        # Check if the user is already following the profile user
        followingList = userFollowingData.followingUsers.all()
        if followingList.filter(username=username).exists():
            message = True
        else: message = False

        return JsonResponse({"is being followed": message}, status=201)
    
    if request.method == "POST":
        if request.user.username == username:
            return JsonResponse({"error": "Sorry, you can't follow yourself."}, status=400)
        else:
            userToFollow = User.objects.get(username=username) # Get User to follow
            userFollowingData = Following.objects.get(follower=request.user) # Get Following object from the current logged user

            # Check if the user is already following the profile user
            followingList = userFollowingData.followingUsers.all()
            if followingList.filter(username=username).exists():
                userFollowingData.followingUsers.remove(userToFollow) # Add the User to follow to the Following
                return JsonResponse({"message": "Current profile has been unfollowed."}, status=201)
            else:
                userFollowingData.followingUsers.add(userToFollow) # Add the User to follow to the Following
                return JsonResponse({"message": "Current profile is now being followed."}, status=201)

    return JsonResponse({"error": "POST or GET request required."}, status=400)


def comments(request, postId):

    if request.method == 'GET':
        comments = Comment.objects.filter(post=postId).all()
        comments = comments.order_by('timestamp')

        commentsDict = {}
        for idx, comment in enumerate(comments):
            commentsDict[idx] = {"user": comment.user.username, "comment": comment.comment, "timestamp": comment.timestamp.timestamp()}

        print(commentsDict)
            
        return JsonResponse(json.dumps(commentsDict), status=201, safe=False)

    if request.method == 'POST':

        # Get comment from JSON
        post_data = json.loads(request.body.decode("utf-8"))
        comment_text = post_data['comment']

        # Create comment Object
        postIntance = Post.objects.get(id=postId)
        comment_obj = Comment(user=request.user, post=postIntance, comment=comment_text)
        comment_obj.save()

        return JsonResponse({"message": "comment sent succesfully"}, status=201)