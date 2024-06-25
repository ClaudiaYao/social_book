from django.db import models
from django.contrib.auth.models import User 
import uuid 

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.IntegerField(primary_key=True)
    bio = models.TextField(null=True, blank=True)
    profileimg = models.ImageField(null=True, blank=True, upload_to="profile_images/", default="default_user.jpg")
    cover_photo = models.ImageField(null=True, blank=True, upload_to="cover_images/", default="default_cover_image.jpg")
    location = models.CharField(max_length=200, null=True, blank=True)
    no_of_followers = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username)
    
class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="post_images/")
    caption = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.caption)
    
class LikePost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    
    # id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.owner.username)
    
    class Meta:
        unique_together = [['owner', 'post']]


class FollowersCount(models.Model):
    follower = models.CharField(max_length=200)
    user = models.CharField(max_length=200)

    def __str__(self):
        return str(self.follower)
    
    class Meta:
        unique_together = [['follower', 'user']]


