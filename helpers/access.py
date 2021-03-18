from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions


class AccessEditAuthor(permissions.BasePermission):
    """
    Доступ к созданию, обновлению, удалению только у авторов.
    """
    def has_permission(self, request, view):

        user = request.user
        if request.method == 'POST':
            if view.kwargs:
                try:
                    obj = view.queryset.get(pk=view.kwargs['pk'])
                except ObjectDoesNotExist:
                    return False
                return user.is_author and obj.author == user
            if user and user.is_authenticated:
                return user.is_author
            else:
                return False
        elif request.method in ['PUT', 'DELETE', 'PATCH']:
            if view.kwargs:
                try:
                    obj = view.queryset.get(pk=view.kwargs['pk'])
                except ObjectDoesNotExist:
                    return False
                return user == obj.author
        else:
            if view.kwargs:
                return user.is_authenticated
            else:
                if request.method in permissions.SAFE_METHODS:
                    return bool(request.user and request.user.is_authenticated)
                else:
                    return False


class IsSuperUser(permissions.BasePermission):
    """Разрешается доступ только супер-пользователям"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class ReadOnly(permissions.BasePermission):
    """Используется если view доступен только для чтения всем. """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return request.user.is_superuser
