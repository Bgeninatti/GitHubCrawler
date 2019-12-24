
from lxml import etree
from logger import get_logger
from crawler.cfg import BASE_URL

logger = get_logger(__name__)


class GitHubSearchParser:
    """
    Crawler for GitHub search.
    """
    xpaths = {
        'wikis': "//div[contains(@class,'wiki-list-item')]/div/div/a[2]/@href",
        'repositories': "//li[contains(@class,'repo-list-item')]/div[1]/h3/a/@href",
        'issues': "//div[contains(@class,'issue-list-item')]/div/div[1]/h3/a/@href"
    }

    def __init__(self, url, content, result_type):
        """
        Initialize a search with parameters and a handler that will be used
        to make the request.

              :param query: string of keywords. Each keyword should be separated by a '+' sign.
                            i.e: For keywords "python" and "html" `query` param will be "python+html"
              :type query: string
              :param result_type: One of the three supported result types: `wikis`, `repositories`, `issues`
              :type result_type: str
              :param http_handler: An instance of any class with a `get(url)` method that
                                   gets an url as argument and return a redeable object with HTML content
        """
        self.url = url
        self._htmlparser = etree.HTMLParser()
        self._result_tree = etree.parse(content, self._htmlparser)
        if result_type.lower() not in self.xpaths.keys():
            raise ValueError("Result of type \"{}\" is not supported".format(
                result_type))
        self.result_type = result_type.lower()
        logger.info("GitHubSearchCrawler initialized: url=%s, result_type=%s",
                    self.url, self.result_type)

    def get_result(self):
        """
        This method should be run after the `self.run()` method.
        Search the links for each search result based on the result_type.

          :return: list of dict like: `{"url": "http://github.com/some_result"}`
          :rtype: list of dicts
        """
        logger.info("Searching results in HTML tree: result_type=%s", self.result_type)
        xpath = self.xpaths[self.result_type]
        urls = self._result_tree.xpath(xpath)
        results = [{"url": f"{BASE_URL}{url}"} for url in urls]
        logger.info("Results found: result_type=%s, result_count=%d",
                    self.result_type, len(results))
        return results


class GitHubRepoStatsParser:

    xpaths = {
        'owner': "//span[contains(@class, 'author')]/a/text()",
        'languages': "//span[contains(@class, 'language-color')]/@aria-label"
    }

    def __init__(self, url, content):
        """
        Initialize a search with parameters and a handler that will be used
        to make the request.

              :param query: string of keywords. Each keyword should be separated by a '+' sign.
                            i.e: For keywords "python" and "html" `query` param will be "python+html"
              :type query: string
              :param result_type: One of the three supported result types: `wikis`, `repositories`, `issues`
              :type result_type: str
              :param http_handler: An instance of any class with a `get(url)` method that
                                   gets an url as argument and return a redeable object with HTML content
        """
        self.url = url
        self._htmlparser = etree.HTMLParser()
        self._result_tree = etree.parse(content, self._htmlparser)
        logger.info("GitHubReposStatsCrawler initialized: url=%s", self.url)

    def get_result(self):
        """
        Search in the repository main page extra data related to the repo.
        Returns a dict like:

        ```
        {
          'owner': "OwnerName",
          'language_stats': {
            'language_1': xx.x,
            'language_2': yy.y,
            ...
          }
        }
        ```
        """
        result = {}
        owner_search = self._result_tree.xpath(self.xpaths['owner'])
        result['owner'] = owner_search[0] if owner_search else None
        languages = [txt.split(' ') for txt in
                     self._result_tree.xpath(self.xpaths['languages'])]
        result['language_stats'] = {lan[0]: float(lan[-1].replace('%', ''))
                                    for lan in languages}

        return result
