from rest_framework import permissions
from rest_framework.generics import get_object_or_404


class AccessEdit(permissions.BasePermission):
    """
    Используется для view, у которых поле 'user' приходит в body POST-запроса
    или поле c id объекта, имеющего поле 'user', приходит в URL запроса (в kwargs) для остальных запросов.
    """
    def has_permission(self, request, view):

        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            user = request.user
            if user and user.is_authenticated:
                return user.is_author
            else:
                return False
        else:
            if view.kwargs:
                obj = get_object_or_404(view.queryset, pk=view.kwargs['pk'])
                user = obj.author.user
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
