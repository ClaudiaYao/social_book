from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Profile, Post, LikePost, FollowersCount
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="signin")
def index(request):
    user_profile = Profile.objects.get(user=request.user)

    following_post = []
    user_following = FollowersCount.objects.filter(follower = user_profile.id)
    followed_profile_id = []
    for following in user_following:
        # each object in user_following stores follower's profile id and followed's profile id
        followed_profile = Profile.objects.get(id = following.user)
        followed_profile_id.append(followed_profile.id)
        posts = Post.objects.filter(profile = followed_profile)
        following_post.extend(posts)

    # user's own posts
    posts = Post.objects.filter(profile=user_profile)
    following_post.extend(posts)

    suggested_profiles = Profile.objects.all().exclude(id__in=followed_profile_id)
    suggested_profiles = suggested_profiles.exclude(id=user_profile.id)

    like_posts = LikePost.objects.filter(owner=request.user)
    like_post_ids = []
    for like_post in like_posts:
        like_post_ids.append(like_post.post.id)

    return render(request, "index.html", context={"profile": user_profile, "posts": following_post, "suggested_profiles": suggested_profiles, "like_post_ids": like_post_ids})

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email has existed.")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "User name has existed.")
                return redirect("signup")
            else:
                # create new user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # make the new user login in
                user = authenticate(request, username=username, email=email, password=password)
                login(request, user)

                # create profile
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user= user_model.id)
                new_profile.save()
                return redirect("signin")
        else:
            messages.info(request, "Password does not match.")
            return redirect("signup")

    else:
        return render(request, "signup.html")
    

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "User name or password does not exist!")
            return redirect('signin')
    else:
        return render(request, "signin.html")

@login_required(login_url="signin")
def signout(request):
    logout(request)
    messages.info(request, "User was logged out.")
    return redirect("signin")

@login_required(login_url="signin")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    print(user_profile)

    if request.method == "POST":
        if request.FILES.get('image') is not None:
            user_profile.profileimg = request.FILES.get('image')
          
        user_profile.bio = request.POST['bio']
        user_profile.location = request.POST['location']
        user_profile.save()
        return redirect("index")
        
    return render(request, "setting.html", context = {"profile": user_profile})

@login_required(login_url="signin")
def upload(request):
    if request.method == "POST":
        profile = Profile.objects.get(user = request.user)
        image = request.FILES.get("image_upload")
        caption = request.POST['caption']

        print(image)
        print(caption)
        if (image is None) and (caption==""):
            return redirect("index")

        new_post = Post.objects.create(profile = profile, image=image, caption=caption)
        new_post.save()
        messages.info(request, "Post has been created successfully.")
        return redirect("index")

    return redirect("index")

@login_required(login_url="signin")
def like_post(request, post_id):
    
    user = request.user
    post_to_edit = Post.objects.get(id=post_id)

    likepost = LikePost.objects.filter(owner=user, post=post_to_edit).first()
    
    if likepost is None:
        new_likepost = LikePost.objects.create(owner=user, post=post_to_edit)
        new_likepost.save()

        post_to_edit.no_of_likes += 1
        post_to_edit.save()
    else:
        likepost.delete()
        post_to_edit.no_of_likes -= 1
        post_to_edit.save()

    return redirect("index")

@login_required(login_url="signin")
def profile(request, profile_id):
    chosen_profile = Profile.objects.get(id = profile_id)
    follower_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(profile = chosen_profile)

    if FollowersCount.objects.filter(follower=follower_profile.id, user=chosen_profile.id):
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    follower_num = len(FollowersCount.objects.filter(follower=profile_id))
    following_num = chosen_profile.no_of_followers
    return render(request, "profile.html", context= {"profile": chosen_profile, "posts": posts, "post_count": len(posts), "button_text": button_text, "following_num": following_num})

@login_required(login_url="signin")
def follow(request, followed_profile_id):
    print("enter function")
    follower_profile = Profile.objects.get(user=request.user)
    followed_profile = Profile.objects.get(id=followed_profile_id)

    follower = FollowersCount.objects.filter(follower=follower_profile.id, user = followed_profile.id).first()
    
    if follower is None:
        print("generated new follower")
        new_follower = FollowersCount.objects.create(follower=follower_profile.id, user = followed_profile.id)
        new_follower.save()

        followed_profile.no_of_followers += 1
        followed_profile.save()
    else:
        print("unfollow existing user")
        follower.delete()
        followed_profile.no_of_followers -= 1
        followed_profile.save()

    if "profile" in request.path:
        return redirect("profile", profile_id=followed_profile_id)
    else:
        return redirect("index")

# @login_required(login_url="signin")
# def edit_post(request):

@login_required(login_url="signin")
def search(request):
    if request.method == "POST":
        user_profile = Profile.objects.get(user = request.user)
        username = request.POST['username']
        searched_users = User.objects.filter(username__icontains = username)
        
        searched_profiles = Profile.objects.filter(user__in=searched_users)
        
    return render(request, "search.html", context={"user_profile": user_profile, "searched_profiles": searched_profiles})
    
