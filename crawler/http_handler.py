import urllib.parse
import urllib.request
import urllib.error
import concurrent.futures
from logger import get_logger

logger = get_logger(__name__)


class UrllibHandler:
    """
    Http handler that uses urllib and allow proxies
    """

    def __init__(self, url, proxy=None, **kwargs):
        """
        Initialize the http handler. A proxies list with the format
        "ip:port" can be provided.
        If the proxies list is provided, a random proxy will be selected
        to make each request.
          :param proxies: list of strings with format "ip:port"
          :type query: list of strings
        """
        self.proxy = proxy
        self.query_params = urllib.parse.urlencode(kwargs)
        self.url = url if not self.query_params else f"{url}?{self.query_params}"
        logger.info("UrllibHandler initialized: url=%s, proxy=%s", self.url, self.proxy)

    def get(self):
        """
        Get a url and return a redeable object with the raw html retrived
        """
        request = urllib.request.Request(self.url)
        if self.proxy:
            request.set_proxy(self.proxy, 'http')
        logger.info("Attempt to do GET request: url=%s, proxy=%s",
                    self.url, self.proxy)
        response = urllib.request.urlopen(request)
        logger.info("GET request was successful: url=%s, proxy=%s",
                    self.url, self.proxy)
        return response


def get_urls_async(urls, proxy, max_workers=8):
    result = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for url in urls:
            handler = UrllibHandler(url, proxy)
            future = executor.submit(handler.get)
            futures[future] = url

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                response = future.result()
            except (urllib.error.URLError, urllib.error.HTTPError) as ex:
                logger.error("Unexpected error during request: url=%s, proxy=%s, " + \
                             "error=%s", url, proxy, ex)
                response = None

            result[url] = response
    return result
