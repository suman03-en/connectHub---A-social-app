from django import template

register = template.Library()

@register.filter()
def liked_by(post,user):
    return post.likes.filter(user=user).exists()
