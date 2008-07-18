from django.template import Library
from django.conf import settings

register = Library()

def graphics_url_prefix():
    """url prefix for js lib.
    
    settings.GRAPHICS_JS_URL must be set.
    A suitable value is "http://www.walterzorn.com/scripts/"
    """
    return settings.GRAPHICS_JS_URL
graphics_url_prefix = register.simple_tag(graphics_url_prefix)
