from django import template
register = template.Library()

@register.filter
def dict_get(dict, key):
    return dict.get(str(key), [])