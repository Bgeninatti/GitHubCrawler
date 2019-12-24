import urllib.parse
import urllib.request
import urllib.error
import concurrent.futures
from logger import get_logger
from crawler.cfg import MAX_HTTP_WORKERS

logger = get_logger(__name__)


class UrllibHandler:
    """
    Http handler that uses urllib and allow proxies
    """

    def __init__(self, url, proxy=None, **kwargs):
        """
        Initialize the http handler to perform requests in a URL.
        A proxy with the format "ip:port" can be provided.
        All the extra arguments (kwargs) will be parsed and sent as
        GET parameters in the request.
          :param url: URL to perform the request
          :type url: string
          :param proxy: string with format "ip:port"
          :type query: string
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


def get_urls_async(urls, proxy=None, max_workers=MAX_HTTP_WORKERS):
    """
    Perform async requests on each url in urls and return the result.
    The max number of concurrent requests is controled by `max_workers`
    If a proxy is provided, it will be used to make all the requests.

    Return a dictionary with `url` as key and the resultant requests as value
    (or None if an exception is rised during request)
    """
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
