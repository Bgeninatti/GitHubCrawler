import pytest
import urllib.parse
from crawler.http_handler import UrllibHandler, get_urls_async


class TestUrllibHandler:

    def test_get_return_redeable_object(self):
        handler = UrllibHandler("https://stackoverflow.com/")
        response = handler.get()
        assert hasattr(response, 'read')

    @pytest.mark.parametrize("kwargs", [
        {'arg1': "arg", 'arg2': 'value'},
        {'key': "value", 'int': "123", 'float': "1.2"},
    ])
    def test_kwargs_as_query_params(self, kwargs):
        handler = UrllibHandler("https://stackoverflow.com/", **kwargs)
        parsed_url = urllib.parse.urlparse(handler.url)
        query = urllib.parse.parse_qs(parsed_url.query)
        assert kwargs.keys() == query.keys()
        for k, v in query.items():
            assert v[0] == kwargs[k]

    @pytest.mark.parametrize("value, key, encoded_query", [
        ("#", "q", "q=%23"),
        ("¥", "q", "q=%C2%A5"),
        ("ê", "q", "q=%C3%AA"),
        ("ý", "q", "q=%C3%BD")
    ])
    def test_kwargs_support_unicode(self, value, key, encoded_query):
        kwargs = {}
        kwargs[key] = value
        handler = UrllibHandler("https://stackoverflow.com/", **kwargs)
        parsed_url = urllib.parse.urlparse(handler.url)
        assert parsed_url.query == encoded_query


class TestGetUrlsAsync:

    @pytest.mark.parametrize("urls", [
        ["https://stackoverflow.com/",
         "https://google.com",
         "https://github.com",
         "https://bgeninatti.com"],
        ["http://isnotavalidurl",
         "http://butshouldworkanyway",
         "http://logtherrorandexit"],
    ])
    def test_return_dict_of_urls(self, urls):
        results = get_urls_async(urls)
        for url in urls:
            assert url in results.keys()
