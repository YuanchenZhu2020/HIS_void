from django import template

register = template.Library()

@register.filter(name = "get_range")
def get_range(value, st = 1):
    return range(st, value + st)
