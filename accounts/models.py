from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,AbstractUser
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password):
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255,unique=True,blank=False)
    first_name = models.CharField(max_length=250,blank=False)
    last_name = models.CharField(max_length=250,blank=False)
    profile_pic = models.ImageField(upload_to='accounts/profile/',blank=True,null=True)
    bio = models.CharField(max_length=150,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField(
        "self",
        related_name="followers",
        symmetrical=False,
        blank=True
        )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        indexes = [
            models.Index(fields=['username'])
        ]

    def follow(self,user):
        if self != user and not self.is_following(user):
            self.following.add(user)
            self.save()
    
    def unfollow(self,user):
        if self.is_following(user):
            self.following.remove(user)
            self.save()

    def is_following(self,user):
       return self.following.filter(username=user.username).exists()
    
    def follower_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()

    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.username})
    
    
