from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions


class AccessEditAuthor(permissions.BasePermission):
    """
    Используется для view, у которых поле 'user' приходит в body POST-запроса
    или поле c id объекта, имеющего поле 'user', приходит в URL запроса (в kwargs) для остальных запросов.
    """
    def has_permission(self, request, view):

        user = request.user
        if request.method == 'POST':
            if view.kwargs:
                try:
                    obj = view.queryset.get(pk=view.kwargs['pk'])
                except ObjectDoesNotExist:
                    return False
                return user.is_author and obj.author.user == user
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
                return user == obj.author.user
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
