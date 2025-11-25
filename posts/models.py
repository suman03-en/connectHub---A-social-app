from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = ThumbnailerImageField(upload_to="posts/images/",resize_source=dict(size=(400, 400), quality=85),blank=True,null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE
    )
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} created by {self.created_by.first_name+" "+self.created_by.first_name}"

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','post')

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
    
class Comment(models.Model):
    text = models.CharField(blank=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
        )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)





