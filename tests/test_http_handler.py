import pytest
from crawler.http_handler import UrllibHandler


class TestUrllibHandler:

    def test_get_return_redeable_object(self):
        handler = UrllibHandler([])
        response = handler.get("https://stackoverflow.com/")
        assert hasattr(response, 'read')

    @pytest.mark.parametrize("query, key, encoded_query", [
        ("#", "q", "q=%23"),
        ("¥", "q", "q=%C2%A5"),
        ("ê", "q", "q=%C3%AA"),
        ("ý", "q", "q=%C3%BD")
    ])
    def test_support_unicode(self, query, key, encoded_query):
        crawler = GitHubSearchCrawler(query, "issues", http_handler)
        assert crawler._query_params == encoded_query
