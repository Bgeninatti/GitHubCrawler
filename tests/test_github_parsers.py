import pytest
import tempfile
import os
from io import StringIO
from crawler.parsers import GitHubSearchParser, GitHubRepoStatsParser
from crawler.http_handler import UrllibHandler

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture
def dummy_html():
    html_file = StringIO("<html></html>")
    return html_file


class TestGitHubSearchParser:

    @pytest.mark.parametrize("result_type", [
        "unsupported",
        "Code",
        "RegistryPackages",
        "Marketplace",
        "Topics",
        "Users"
    ])
    def test_usupported_result_types(self, result_type, dummy_html):
        with pytest.raises(ValueError):
            GitHubSearchParser(dummy_html,
                               result_type)

    @pytest.mark.parametrize("html_file,result_type", [
        ("html_files/result_issues.html", "issues"),
        ("html_files/result_repositories.html", "repositories"),
        ("html_files/result_wikis.html", "wikis"),
    ])
    def test_get_result_return_list_of_objects(self, html_file, result_type):
        path_to_html = os.path.join(BASE_PATH, html_file)
        print(path_to_html)
        parser = GitHubSearchParser(open(path_to_html),
                                    result_type)

        result = parser.get_result()
        assert all(["url" in el.keys() for el in result])


class TestGitHubStatsParser:

    @pytest.mark.parametrize("html_file", [
        "html_files/repo_django.html",
        "html_files/repo_tornado.html",
        "html_files/repo_nvim.html",
    ])
    def test_return_extra_data_object(self, html_file):
        path_to_html = os.path.join(BASE_PATH, html_file)
        parser = GitHubRepoStatsParser(open(path_to_html, "r"))
        result = parser.get_result()
        assert "owner" in result.keys()
        assert "language_stats" in result.keys()
        assert len(result['language_stats'])

