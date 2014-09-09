import re

from django import template
from django.conf import settings

from auth.views import is_admin, _has_perm
from auth import EDIT_GROUPS, EDIT_ROLES

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern):
    request = context['request']
    pattern = '^%s/' + pattern
    if getattr(settings, 'FORCE_SCRIPT_NAME', None):
        pattern = pattern % settings.FORCE_SCRIPT_NAME
    else:
        pattern = pattern % ''

    if re.search(pattern, request.path):
        return 'active'
    return ''


@register.assignment_tag(name='is_admin', takes_context=True)
def do_is_admin(context):
    return True if is_admin(context['request']) else False


@register.assignment_tag(takes_context=True)
def can_edit_entry(context, entry):
    request = context['request']
    if is_admin(request):
        return True
    if _has_perm(request.user_roles, request.user_groups, roles=EDIT_ROLES,
                 groups=EDIT_GROUPS) and request.user_id == entry.user_id:
        return True
    return False
