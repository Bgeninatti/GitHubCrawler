import random
import urllib.parse
import urllib.request
import urllib.error
from logger import get_logger

logger = get_logger(__name__)


class UrllibHandler:
    """
    Http handler that uses urllib and allow proxies
    """

    def __init__(self, proxies=[]):
        """
        Initialize the http handler. A proxies list with the format
        "ip:port" can be provided.
        If the proxies list is provided, a random proxy will be selected
        to make each request.
          :param proxies: list of strings with format "ip:port"
          :type query: list of strings
        """
        self._proxies = proxies

    def get(self, url):
        """
        Get a url and return a redeable object with the raw html retrived
        """
        request = urllib.request.Request(url)
        proxy = self._get_proxy()
        if proxy:
            request.set_proxy(proxy, 'http')
        logger.info("Attempt to do GET request: url=%s, proxy=%s", url, proxy)
        response = urllib.request.urlopen(request)
        logger.info("GET request was successful: url=%s, proxy=%s", url, proxy)
        return response

    def _get_proxy(self):
        """
        Return a random proxy from `self._proxies`. If the proxies list
        is empty return None
        """
        if not self._proxies:
            return
        return random.choice(self._proxies)
