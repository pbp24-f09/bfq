from django import template

register = template.Library()

@register.filter(name='format_idr')
def format_idr(value):
    """Formats a number as IDR with thousands separators."""
    if value is None:
        return ''
    return '{:,.0f}'.format(value).replace(',', '.')  # Replace comma with dot for IDR
