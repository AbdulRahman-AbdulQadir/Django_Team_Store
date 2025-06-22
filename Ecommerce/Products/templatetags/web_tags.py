# your_app_name/templatetags/web_tags.py

from django import template
from django.http import QueryDict # Import QueryDict
from urllib.parse import urlencode # Only need urlencode from urllib.parse

register = template.Library()

@register.filter
def update_query_params(query_dict, kwargs_string):
    """
    Updates the QueryDict with new parameters or removes existing ones.
    Usage: {{ request.GET|update_query_params:"page=1,category=None" }}
    Use 'None' as value to remove a parameter.
    """
    params = query_dict.copy() # Always work on a copy to avoid modifying original request.GET

    # Parse the kwargs_string (e.g., "page=1,category=None")
    kwargs = {}
    for item in kwargs_string.split(','):
        if '=' in item:
            key, value = item.split('=', 1)
            kwargs[key.strip()] = value.strip()
        else:
            # Handle cases where just a key is passed, maybe to indicate removal
            kwargs[item.strip()] = None # Or some other default removal indicator

    for key, value in kwargs.items():
        if value == 'None': # Our special string to indicate removal
            if key in params:
                del params[key]
        else:
            params[key] = value # Update or add the parameter

    return params.urlencode()

@register.filter
def query_string_exclude(query_dict, exclude_keys_string):
    """
    Excludes specified keys from a QueryDict and returns the URL-encoded string.
    Usage: {{ request.GET|query_string_exclude:"page,sort_by" }}
    """
    params = query_dict.copy()
    exclude_keys = [k.strip() for k in exclude_keys_string.split(',')]

    for key in exclude_keys:
        if key in params:
            del params[key]
            
    return params.urlencode()