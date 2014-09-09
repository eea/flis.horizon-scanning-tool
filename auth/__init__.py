from django.conf import settings

_VIEW_ROLES = ('Administrator', 'Contributor',)
VIEW_ROLES = getattr(settings, 'VIEW_ROLES', _VIEW_ROLES)

_EDIT_ROLES = ('Administrator', 'Contributor',)
EDIT_ROLES = getattr(settings, 'EDIT_ROLES', _EDIT_ROLES)

_VIEW_GROUPS = ('eionet-nfp',)
VIEW_GROUPS = getattr(settings, 'VIEW_GROUPS', _VIEW_GROUPS,)

_EDIT_GROUPS = ('eionet-nrc-forwardlooking',)
EDIT_GROUPS = getattr(settings, 'EDIT_GROUPS', _EDIT_GROUPS)

ROLES = VIEW_ROLES + EDIT_ROLES

GROUPS = VIEW_GROUPS + EDIT_GROUPS
