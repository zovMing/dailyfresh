from django.template  import Library
import decimal
register = Library()

@register.filter
def ride(value, v2):
    return float(value) * int(v2)