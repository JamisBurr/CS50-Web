from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Post
from .models import User
import json

# Index view to display posts and handle post submission
def index(request):
    if request.method == "POST":
        # Handle new post submission
        content = request.POST.get('content', '')
        if content:  # Check that content is not empty
            Post.objects.create(user=request.user, content=content)

        # Redirect to the same page after submission to prevent re-submission on refresh
        return redirect('index')

    # Display all posts (for GET requests)
    posts = Post.objects.all().order_by('-timestamp')

    # Set up pagination with 10 posts per page
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the page object to the template
    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


@csrf_exempt
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if request.user in post.likes.all():
            # If the user already liked the post, remove the like (unlike)
            post.likes.remove(request.user)
            liked = False
        else:
            # Add the like
            post.likes.add(request.user)
            liked = True
        
        # Return the updated like count and liked status
        return JsonResponse({
            "message": "Success",
            "likes_count": post.likes.count(),
            "liked": liked  # Whether the post is liked or unliked
        }, status=201)


@csrf_exempt
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only allow the post owner to edit the post
    if request.user != post.user:
        return JsonResponse({"error": "You cannot edit this post."}, status=403)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        new_content = data.get("content", "")
        post.content = new_content
        post.save()
        return JsonResponse({"message": "Post updated successfully."}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)
    

def profile(request, username):
    # Get the user whose profile is being viewed
    profile_user = get_object_or_404(User, username=username)
    
    # Get the number of followers and following
    follower_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    
    # Get the posts of the user
    posts = Post.objects.filter(user=profile_user).order_by('-timestamp')

    # Check if the current user follows this profile user
    is_following = request.user in profile_user.followers.all()
    
    # Render the profile.html template
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "follower_count": follower_count,
        "following_count": following_count,
        "posts": posts,
        "is_following": is_following
    })

@login_required
@csrf_exempt
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.method == "POST":
        if request.user in target_user.followers.all():
            # Unfollow
            request.user.following.remove(target_user)
            is_following = False
        else:
            # Follow
            request.user.following.add(target_user)
            is_following = True

        # Return the updated follower count and follow status
        return JsonResponse({
            "is_following": is_following,
            "follower_count": target_user.followers.count()
        }, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def following(request):
    # Get the users that the current user is following
    followed_users = request.user.following.all()

    # Get the posts from those followed users
    posts = Post.objects.filter(user__in=followed_users).order_by('-timestamp')

    # Set up pagination with 10 posts per page
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the page object to the template
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
