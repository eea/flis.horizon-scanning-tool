from django import template
from django.utils.safestring import mark_safe
from django.db.models import Q

from hstool.definitions import RELATION_TYPE_CHOICES
from hstool.models import Assessment

register = template.Library()


@register.filter(name='label')
def render_label(field, required=False):
    return mark_safe(
        field.label + (
            ' <span class="text-danger">*</span>'
            if field.field.required or required else ''
        )
    )


@register.filter(name='is_filefield')
def is_filefield(field):
    return field.label == 'File'


@register.filter(name='verbose')
def verbose(relation_type):
    choices = dict(RELATION_TYPE_CHOICES)
    return choices.get(int(relation_type), relation_type)


@register.filter()
def file_type(filefield):
    extension = filefield.name.split('.')[-1]
    return extension


@register.assignment_tag()
def assessment_usages(generic_element, assessment):
    assessments = (
        Assessment.objects
        .filter(Q(relations__source=generic_element) |
                Q(relations__destination=generic_element))
        .exclude(pk=assessment.pk)
        .all()
    )
    return set(assessments)
