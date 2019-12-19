import random
import urllib.parse
import urllib.request
from lxml import etree
from collections import defaultdict
from logger import get_logger

BASE_URL = "https://github.com"
logger = get_logger(__name__)


class HTTPHandler:

    def __init__(self, proxies):
        self._proxies = proxies

    def get(self, url):
        proxy = self._get_proxy()
        request = urllib.request.Request(url)
        request.set_proxy(proxy, 'http')
        logger.info("Attempt to do GET request: url=%s, proxy=%s", url, proxy)
        response = urllib.request.urlopen(request)
        logger.info("GET request was successful: url=%s, proxy=%s", url, proxy)
        return response

    def _get_proxy(self):
        return random.choice(self._proxies)


class GitHubSearchCrawler:
    """
    Crawl
    """
    search_uri = '/search'
    xpaths = {
        'wikis': "//div[contains(@class,'wiki-list-item')]/div/div/a[2]/@href",
        'repositories': "//li[contains(@class,'repo-list-item')]/div[1]/h3/a/@href",
        'issues': "//div[contains(@class,'issue-list-item')]/div/div[1]/h3/a/@href"
    }

    def __init__(self, query, result_type, http_handler):
        if result_type.lower() not in self.xpaths.keys():
            raise ValueError("Result of type \"{}\" is not supported".format(
                result_type))
        self.query = query
        self.result_type = result_type.lower()
        self._query_params = urllib.parse.quote(query)

        self._url = f"{BASE_URL}{self.search_uri}" + \
                    f"?q={self._query_params}&type={self.result_type}"
        self._http_handler = http_handler
        self._htmlparser = etree.HTMLParser()
        self._result_tree = None
        logger.info("GitHubSearchCrawler initialized: query=%s, result_type=%s",
                    self.query, self.result_type)

    def run(self):
        """
        Run crawler, download data and parse the result as HTML.
        """
        response = self._http_handler.get(self._url)
        logger.info("Parsing HTML tree from HTTP response")
        self._result_tree = etree.parse(response, self._htmlparser)

    def get_result(self):
        logger.info("Searching results in HTML tree: result_type=%s", self.result_type)
        xpath = self.xpaths[self.result_type]
        urls = self._result_tree.xpath(xpath)
        results = [{"url": f"{BASE_URL}{url}"} for url in urls]
        logger.info("Results found: result_type=%s, result_count=%d",
                    self.result_type, len(results))
        return results
