from django.template import Library
register = Library()

@register.filter
def ned(vale, num):
    return vale[0:int(num)]

@register.filter
def add(value, va):
    if value == '':
        return 0
    t = int(value)    
    t += va
    
    if t <= 0:
        return 1
    return str(t)