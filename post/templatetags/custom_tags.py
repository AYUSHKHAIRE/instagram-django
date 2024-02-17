from django import template
from django.contrib.auth.models import User
register = template.Library()


@register.simple_tag
def get_profile_image_url(user):
    return user.profile.image.url if hasattr(user, 'profile') else None
