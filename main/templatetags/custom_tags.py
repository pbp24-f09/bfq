from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    attrs = {
        "class": css_class,
        "oninput": "toggleInputColor(this)"
    }
    return field.as_widget(attrs=attrs)
