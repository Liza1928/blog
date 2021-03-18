from helpers.access import AccessEditAuthor, IsSuperUser
from unittest.mock import Mock


class UserMock:
    def __init__(
            self, id=1, is_authenticated=False, is_superuser=False, is_author=False
    ):
        self.id = id
        self.is_authenticated = is_authenticated
        self.is_superuser = is_superuser
        self.is_author = is_author


class RequestMock:
    def __init__(self, user, method, data=None):
        self.user = user
        self.method = method
        self.data = data


class MockPost:
    author = None

    def __init__(self, author):
        self.author = author
        self.DoesNotExist = True


class MockPostQuerySet(object):
    model = MockPost
    
    def get(self, **kwargs):
        return self.model


class ViewMock:
    def __init__(self, kwargs=None, queryset=None):
        self.kwargs = kwargs
        self.queryset = queryset


class ObjectMock:
    def __init__(self, user):
        self.user = user


class TestAccessEditAuthor:
    view = ViewMock()
    authenticated_user = UserMock(is_authenticated=True)
    not_authenticated_user = UserMock()
    author_user = UserMock(is_authenticated=True, is_author=True)
    super_user = UserMock(is_superuser=True)
    user_to_access_not_your_post = UserMock(id=2, is_authenticated=True, is_author=True)
    post = MockPost(author=author_user)

    # AccessEdit
    def test_access_edit_get_not_authenticated(self):
        request = RequestMock(self.not_authenticated_user, 'GET')
        assert not AccessEditAuthor().has_permission(request, self.view)

    def test_access_edit_get_authenticated(self):
        request = RequestMock(self.authenticated_user, 'GET')
        assert AccessEditAuthor().has_permission(request, self.view)

    def test_access_edit_put(self):
        request = RequestMock(self.authenticated_user, 'PUT')
        assert not AccessEditAuthor().has_permission(request, self.view)

    def test_access_edit_post(self):
        request = RequestMock(self.author_user, 'POST')
        assert AccessEditAuthor().has_permission(request, self.view)

    def test_access_edit_post_another_user(self):
        post_mock = Mock()
        post_mock.get.return_value = self.post
        view_with_pk = ViewMock(kwargs={'pk': '1'}, queryset=post_mock)
        request = RequestMock(self.user_to_access_not_your_post, 'POST')
        assert not AccessEditAuthor().has_permission(request, view_with_pk)

    # IsSuperUser
    def test_is_super_user(self):
        request = RequestMock(self.authenticated_user, 'GET')
        assert not IsSuperUser().has_permission(request, self.view)

    def test_is_not_super_user(self):
        request = RequestMock(self.super_user, 'GET')
        assert IsSuperUser().has_permission(request, self.view)
