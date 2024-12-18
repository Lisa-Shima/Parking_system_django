from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """
    Add a CSS class to form input fields dynamically.
    """
    existing_classes = value.field.widget.attrs.get('class', '')
    value.field.widget.attrs['class'] = f"{existing_classes} {css_class}".strip()
    return value