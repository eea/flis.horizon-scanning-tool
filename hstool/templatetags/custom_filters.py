from django import template
from django.utils.safestring import mark_safe

from hstool.definitions import RELATION_TYPE_CHOICES

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


@register.filter(name='verbose')
def verbose(relation_type):
    choices = dict(RELATION_TYPE_CHOICES)
    return choices.get(int(relation_type), relation_type)
