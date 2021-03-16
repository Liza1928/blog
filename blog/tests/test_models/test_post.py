import pytest


@pytest.mark.usefixtures('create_post')
@pytest.mark.django_db
class TestPostModel:
    pass