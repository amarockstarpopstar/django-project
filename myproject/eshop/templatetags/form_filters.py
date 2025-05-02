from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    """
    Adds a CSS class to a form field.
    Usage: {{ form.field|addclass:"form-control" }}
    """
    return value.as_widget(attrs={'class': arg}) 