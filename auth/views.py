from functools import partial
from django.shortcuts import render
from django.conf import settings
from . import VIEW_ROLES, VIEW_GROUPS, EDIT_GROUPS, EDIT_ROLES


def _has_perm(user_roles, user_groups, roles, groups):
    for user_role in user_roles:
        if user_role in roles:
            return True
    for user_group in user_groups:
        if user_group[0] in groups:
            return True
    return False


def is_admin(request):
    user_id = getattr(request, 'user_id', None)
    user_roles = getattr(request, 'user_roles', [])
    if user_id and 'Administrator' in user_roles:
        return True
    return False


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        dispatch = partial(super(LoginRequiredMixin, self).dispatch,
                           request, *args, **kwargs)
        if settings.SKIP_EDIT_AUTH:
            return dispatch()

        has_perm = _has_perm(request.user_roles, request.user_groups,
                             roles=VIEW_ROLES + EDIT_ROLES,
                             groups=VIEW_GROUPS + EDIT_GROUPS)
        if not (request.user_id and has_perm):
            return render(request, 'auth/restricted.html')

        return dispatch()


class EditPermissionRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        dispatch = partial(super(EditPermissionRequiredMixin, self).dispatch,
                           request, *args, **kwargs)
        if settings.SKIP_EDIT_AUTH:
            return dispatch()

        if not _has_perm(request.user_roles, request.user_groups,
                         roles=EDIT_ROLES,
                         groups=EDIT_GROUPS):
            return render(request, 'auth/restricted.html')

        return dispatch()


class AdminPermissionRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        dispatch = partial(super(AdminPermissionRequiredMixin, self).dispatch,
                           request, *args, **kwargs)
        if settings.SKIP_EDIT_AUTH:
            return dispatch()

        if not (request.user_id and is_admin(request)):
            return render(request, 'auth/restricted.html')

        return dispatch()
