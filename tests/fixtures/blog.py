import pytest
from django.contrib.auth import get_user_model
from crequest.middleware import CrequestMiddleware

from blog.models import Post, Category, Author


User = get_user_model()


@pytest.fixture(autouse=True)
def mock_crequest(request, monkeypatch):
    def mock(*args, **kwargs):
        class MockCrequest:
            path_info = ''
            user = getattr(request.cls, 'user1', None)

        return MockCrequest()

    monkeypatch.setattr(CrequestMiddleware, 'get_request', mock)


@pytest.fixture
def create_users(request):
    request.cls.user1 = User.objects.create_user(
        username='test_user1',
        is_author=True,
        password='1234'
    )
    request.cls.user2 = User.objects.create_user(
        username='test_user2',
        is_author=False,
        password='1234'
    )
    request.cls.user3 = User.objects.create_user(
        username='test_user1',
        is_superuser=True,
        password='1234'
    )


@pytest.fixture
def create_category(request):
    request.cls.category1 = Category.objects.create(name='name1')
    request.cls.category2 = Category.objects.create(name='name2')


@pytest.fixture
def create_post(request):
    request.cls.category1 = Category.objects.create(name='name1')
    request.cls.category2 = Category.objects.create(name='name2')