import os
import json
import pytest
from crawler.crawler import get_repositories_data, do_github_search, parse_input_file

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

class TestParseInputFile:

    @pytest.mark.parametrize("json_file", [
        "input_files/sample_input.json",
    ])
    def test_output(self, json_file):
        path_to_json = os.path.join(BASE_PATH, json_file)
        keywords, result_type, proxies = parse_input_file(path_to_json)
        assert all(isinstance(k, str) for k in keywords)
        assert isinstance(result_type, str)
        assert isinstance(proxies, list)

    @pytest.mark.parametrize("json_file", [
        "input_files/do_not_exists.json",
    ])
    def test_json_do_not_exists(self, json_file):
        path_to_json = os.path.join(BASE_PATH, json_file)
        with pytest.raises(FileNotFoundError):
            parse_input_file(path_to_json)

    @pytest.mark.parametrize("json_file", [
        "input_files/invalid_json.json",
    ])
    def test_invalid_json(self, json_file):
        path_to_json = os.path.join(BASE_PATH, json_file)
        with pytest.raises(json.JSONDecodeError):
            parse_input_file(path_to_json)

    @pytest.mark.parametrize("json_file", [
        "input_files/missing_keys.json",
    ])
    def test_required_parameters(self, json_file):
        path_to_json = os.path.join(BASE_PATH, json_file)
        with pytest.raises(KeyError):
            parse_input_file(path_to_json)

class TestGetRepositoriesData:

    @pytest.mark.parametrize("urls,proxy", [
        (["https://github.com/django/django",
          "https://github.com/neovim/neovim"], None),
    ])
    def test_return_owner_and_stats(self, urls, proxy):
        result = get_repositories_data(urls, proxy)
        print(result)
        assert all("url" in el.keys() for el in result)
        assert all("extra" in el.keys() for el in result)
        assert all("owner" in el["extra"].keys() for el in result)
        assert all("language_stats" in el["extra"].keys() for el in result)

    @pytest.mark.parametrize("urls,proxy", [
        (["https://github.com",
          "https://stackoverflow.com"], None),
    ])
    def test_if_not_a_repo_return_none(self, urls, proxy):
        result = get_repositories_data(urls, proxy)
        assert all(el["extra"]["owner"] is None for el in result)
        assert all(not el["extra"]["language_stats"] for el in result)


class TestDoGithubSearch:

    @pytest.mark.parametrize("keywords, result_type, proxy", [
        (["#", "Pythón"], "issues", None),
        (["¥stringá", "weird"], "repositories", None),
        (["ê", "html", "css"], "wikis", None),
    ])
    def test_return_list_of_objects_with_urls(self, keywords, result_type, proxy):
        result = do_github_search(keywords, result_type, proxy)
        assert all("url" in el.keys() for el in result)
