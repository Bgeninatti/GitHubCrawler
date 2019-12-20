import pytest
from crawler.http_handler import UrllibHandler


class TestUrllibHandler:

    def test_get_return_redeable_object(self):
        handler = UrllibHandler([])
        response = handler.get("https://stackoverflow.com/")
        assert hasattr(response, 'read')
