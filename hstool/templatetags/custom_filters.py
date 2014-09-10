from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='label')
def render_label(field):
    return mark_safe(
        field.label + (
            ' <span class="text-danger">*</span>' if field.field.required
            else ''
        )
    )


@register.filter(name='is_filefield')
def is_filefield(field):
    return field.label == 'File'
