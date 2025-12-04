from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user
from django.db.models import F

from .models import Post,Like,Comment
from .forms import PostCreationForm,CommentCreateForm


@login_required(login_url="login")
def create_post(request):
    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = request.user
            new_post.save()
            return redirect(request.user.get_absolute_url())

    else:
        form = PostCreationForm()

    return render(request, "posts/post/create.html", {"form": form})

@login_required
def edit_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        post_form = PostCreationForm(request.POST,request.FILES,instance=post)
        if post_form.is_valid():
            edited_post = post_form.save(commit=False)
            edited_post.created_by = request.user
            edited_post.save()
            return redirect(request.user.get_absolute_url())
    else:
        post_form = PostCreationForm(instance=post)

    return render(
        request,
        'posts/post/edit.html',
        {'form':post_form}
    )

@login_required
def delete_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if post.created_by == request.user:
        post.delete()
    #add message deleted successfully or  when you can't delete other post
    
    return redirect(request.user.get_absolute_url())



@login_required(login_url='login')
def list_post(request):
    user = get_user(request)
    posts = user.posts.all().select_related("created_by").order_by("-created_at")
    return render(request, "posts/post/list.html", {"user": user, "posts": posts})


@login_required(login_url='login')
@require_POST
def like_action(request):
    post_id = request.POST.get('id')
    post = get_object_or_404(Post,id=post_id)
    current_user = request.user
    action = request.POST.get('action')


    if action == 'like':
        created = Like.objects.filter(post=post,user=current_user).exists()
        if not created:
            Like.objects.create(post=post,user=current_user)
            Post.objects.filter(id=post.id).update(likes_count=F('likes_count') + 1)

        
    elif action == 'unlike':
        deleted_count, _ = Like.objects.filter(post=post,user=current_user).delete()
        if deleted_count > 0:
            Post.objects.filter(id=post.id).update(likes_count=F('likes_count') - 1)

    post.refresh_from_db()
    likes_count = post.likes_count
    
    return JsonResponse({
        "success": True,
        "likes_count": likes_count
    })



@login_required(login_url='login')
def add_comment(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        return redirect('feed')
    
    else:
        form = CommentCreateForm()
    
    return render(
        request,
        "posts/comment/add.html",
       { 
           "post":post,
            "form":form
        }
    )
            
@login_required(login_url='login')
def delete_comment(request,comment_id):
    comment = get_object_or_404(Comment,id=comment_id)
    comment.delete()
    return redirect('feed')