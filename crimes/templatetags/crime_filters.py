from django import template

register = template.Library()

@register.filter
def is_image(value):
    """Check if file is an image based on extension"""
    if not value:
        return False
    return str(value).lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
