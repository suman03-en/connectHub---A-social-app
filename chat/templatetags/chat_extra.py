from django import template

register = template.Library()

@register.filter
def to_string(value, current_username):
    # Get all names excluding the current user
    participants = [user.username for user in value if user.username]
    
    # Return comma-separated others, or empty string if current user is alone
    return ", ".join(participants)
 