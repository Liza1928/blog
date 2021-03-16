from helpers.views import social_authorization_status


class RequestMock:
    def __init__(self, errors):
        if errors:
            self.GET = {'error': ['error']}
        else:
            self.GET = {}


class TestViews:
    def test_with_errors(self):
        request = RequestMock(True)
        response = social_authorization_status(request)
        assert response.content == b'You are NOT logged in'

    def test_without_errors(self):
        request = RequestMock(False)
        response = social_authorization_status(request)
        assert response.content == b'Logging in...'
