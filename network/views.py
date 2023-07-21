from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
import json
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Comment, Like, Follow


def index(request):
    all_posts = Post.objects.all()
    try:
        user = User.objects.get(username=request.user.username)
        user_likes = user.user_like.all()
        user_likes_posts = []
        for user_like in user_likes:
            user_likes_posts.append(user_like.post.id)
    except User.DoesNotExist:
        user_likes_posts = None
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    allposts = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "allposts": allposts,
        "user_likes": user_likes_posts
    })

def following(request):
    try:
        following = request.user.followers.all()
        following_posts = []
        for f in following:
            for following in f.following.post_user.all():
                following_posts.append(following)
    except User.DoesNotExist:
        following_posts = None
    try:
        user = User.objects.get(username=request.user.username)
        user_likes = user.user_like.all()
        user_likes_posts = []
        for user_like in user_likes:
            user_likes_posts.append(user_like.post.id)
    except User.DoesNotExist:
        user_likes_posts = None
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    following_posts = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "allposts": following_posts,
        "user_likes": user_likes_posts
    })

def create_post(request):
    user = request.user
    if request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        post = Post(user=user, title=title, body=body)
        post.save()
        return HttpResponseRedirect(reverse('index'))
    else:    
        return render(request, "network/create.html")

def edit_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        if request.user != post.user:
            return HttpResponseRedirect(reverse('index'))
        elif request.method == "POST":
            post_title = request.POST["title"]
            post_body = request.POST["body"]
            post.title = post_title
            post.body = post_body
            post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "network/edit.html", {
                "post": post
            })
        
    except Post.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))


def comment_post(request, post_id):
    user = request.user
    comment_body = request.POST["comment_body"]
    post = Post.objects.get(pk=post_id)
    comment = Comment(user=user, comment=comment_body, post=post)
    comment.save()
    return HttpResponseRedirect(reverse('index'))

@csrf_exempt
def like(request):
    data = json.loads(request.body)
    user = request.user
    post_id = data.get("post", "")
    post = Post.objects.get(pk=post_id)
    like = Like(user=user, post=post)
    like.save()
    return JsonResponse({"message": "You liked to a post"}, status=201)

@csrf_exempt
def unlike(request):
    data = json.loads(request.body)
    user = request.user
    post_id = data.get("post", "")
    post = Post.objects.get(pk=post_id)
    like = Like.objects.get(user=user, post=post)
    like.delete()
    return JsonResponse({"message": "You unliked to a post"}, status=201)

def myprofile(request):
    user = User.objects.get(username=request.user.username)
    user_likes = user.user_like.all()
    user_likes_posts = []
    for user_like in user_likes:
        user_likes_posts.append(user_like.post.id)
    return render(request, "network/myprofile.html", {
        "user": user,
        "followings": user.followers.all(),
        "followers": user.following.all(),
        "user_likes": user_likes_posts
    })
def user_profile(request, username):
    if username == request.user.username:
        return HttpResponseRedirect(reverse('my_profile'))
    try:
        user = User.objects.get(username=username)
        try:
            follower = Follow.objects.get(following=user, follower=request.user)
        except Follow.DoesNotExist:
            follower = None
    except User.DoesNotExist:
        user = None
    user_likes = request.user.user_like.all()
    user_likes_posts = []
    for user_like in user_likes:
        user_likes_posts.append(user_like.post.id)
    return render(request, "network/user_profile.html", {
        "user_profile": user,
        "username": username,
        "follower": follower,
        "followings": user.followers.all(),
        "followers": user.following.all(),
        "user_likes": user_likes_posts
    })

@csrf_exempt
def follow(request):
    data = json.loads(request.body)
    user = request.user
    following = data.get("following", "")
    following = User.objects.get(username=following)
    follow = Follow(following=following, follower=user)
    follow.save()
    return JsonResponse({"message": "You you are following a user"}, status=201)

@csrf_exempt
def unfollow(request):
    data = json.loads(request.body)
    user = request.user
    following = data.get("following", "")
    following = User.objects.get(username=following)
    unfollow = Follow.objects.get(following=following, follower=user)
    unfollow.delete()
    return JsonResponse({"message": "You unfollowed a user"}, status=201)

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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
