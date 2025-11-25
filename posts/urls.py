from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.create_post,name="create_post"),
    path('<int:post_id>/delete/',views.delete_post,name="post_delete"),
    path('<int:post_id>/edit/',views.edit_post,name="post_edit"),
    path('',views.list_post,name="list_posts"),
    path('<int:post_id>/like_action/',views.like_action,name='like_action'),
    #comments
    path('<int:post_id>/comment/',views.add_comment,name="add_comment"),
    path('comment/<int:comment_id>/delete',views.delete_comment,name="delete_comment"),
]
