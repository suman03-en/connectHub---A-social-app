from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout

from .forms import CustomRegistrationForm,CustomLoginForm,PasswordResetForm,ProfileForm
from .models import CustomUser
from posts.models import Post,Like

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Exists,OuterRef

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

from chat.models import Room

CustomUser = get_user_model()
def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomRegistrationForm()
    return render(
        request,
        'accounts/register.html',
        {
            'form':form
        }
    )

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        email = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect(reverse('feed'))
        
    else:
        form = CustomLoginForm()

    return render(request,'accounts/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect("login")


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get("email")

        try:
            user = CustomUser.objects.get(email=email)
            token =  default_token_generator.make_token(user)  
            uid = urlsafe_base64_encode(force_bytes(user.pk)) 
            reset_link = f'http://127.0.0.1:8000/accounts/reset/{uid}/{token}/'
            send_mail(
                "Password Reset",
                f"Click here to reset your password : {reset_link}",
                'admin@gmail.com',
                [email],
                fail_silently=False
            )
            return redirect('login')
        except CustomUser.DoesNotExist:
            return redirect('password_reset')
        
    return render(request,'accounts/password_reset.html')


def password_reset_confirm(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(id=uid)
    except CustomUser.DoesNotExist:
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        if request.method == "POST":
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data["password1"]
                user.set_password(password)
                user.save()
                return redirect('login')
    if request.method=="GET":
        form = PasswordResetForm()

    return render(
        request,
        'accounts/password_reset_confirm.html',
        {
            "form":form
        }
    )

@login_required(login_url='login')
def profile(request,username):
    profile_user = get_object_or_404(CustomUser,username=username)
    current_user = request.user
    is_following=None
    room_name = Room.generate_room_name(sender=profile_user,receiver=current_user)
    if current_user.is_following(profile_user):
        is_following = True
    posts =profile_user.posts.all().order_by('-created_at')
    return render(
        request,
        'accounts/profile.html',
        {
            'profile_user':profile_user,
            'is_following':is_following,
            'posts':posts,
            'room_name':room_name
        }
    )

@login_required(login_url='login')
def edit_profile(request):
    profile_user = request.user
    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES,instance=profile_user)
        if form.is_valid():
            form.save()
            return redirect(request.user.get_absolute_url())
    else:
        form = ProfileForm(instance=profile_user)
    return render(
        request,
        'accounts/profile_edit.html',
        {
            'form':form,
            'profile_user':profile_user
        }
    )

@login_required(login_url='login')
@require_POST
def follow_action(request,username):
    target_user = get_object_or_404(CustomUser,username=username)
    current_user = request.user
    action = request.POST.get('action')

    if action == 'follow':
        current_user.follow(target_user)
    else:
        current_user.unfollow(target_user)
    return redirect(target_user.get_absolute_url())

@login_required(login_url='login')
def feed(request):
    posts = Post.objects.all().select_related("created_by").order_by('-created_at').annotate(
        is_liked_by_user = Exists(Like.objects.filter(post=OuterRef('pk'),user=request.user))
    )

    return render(
        request,
        'accounts/feed.html',
        {
            'posts':posts
        }
    )


    