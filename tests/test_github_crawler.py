import pytest
from crawler.crawler import GitHubSearchCrawler
from crawler.http_handler import UrllibHandler



@pytest.fixture
def http_handler():
    return UrllibHandler([])


class TestGitHubSearchCrawler:


    @pytest.mark.parametrize("result_type", [
        "unsupported",
        "Code",
        "RegistryPackages",
        "Marketplace",
        "Topics",
        "Users"
    ])
    def test_usupported_result_types(self, result_type, http_handler):
        with pytest.raises(ValueError):
            GitHubSearchCrawler("python", result_type, http_handler)


    @pytest.mark.parametrize("query,encoded_query", [
        ("#", "%23"),
        ("¥", "%C2%A5"),
        ("ê", "%C3%AA"),
        ("ý", "%C3%BD")
    ])
    def test_support_unicode(self, query, encoded_query, http_handler):
        crawler = GitHubSearchCrawler(query, "issues", http_handler)
        assert crawler._query_params == encoded_query


    def test_run_populates_result_tree(self, http_handler):
        crawler = GitHubSearchCrawler("python", "wikis", http_handler)
        crawler.run()
        assert hasattr(crawler._result_tree, 'xpath')

    @pytest.mark.parametrize("result_type", [
        "Issues",
        "Repositories",
        "Wikis"
    ])
    def test_get_result_return_list_of_objects(self, result_type, http_handler):
        crawler = GitHubSearchCrawler("python", result_type, http_handler)
        crawler.run()
        result = crawler.get_result()
        assert all(["url" in el.keys() for el in result])

