from django import template

register = template.Library()

@register.filter
def clp(valor):
    try:
        return f"${int(valor):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "$0"