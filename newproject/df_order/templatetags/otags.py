from django.template import Library
register = Library()

@register.filter
def over(value, id):
    if len(value) > 1:
        return value[0:int(id)]+'...'  
    else:
        return ''