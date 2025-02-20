import json
from django import template

register = template.Library()

@register.filter
def get_json(value):
    return json.dumps(value)
