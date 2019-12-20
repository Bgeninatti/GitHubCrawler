import random
import urllib.parse
import urllib.request
import urllib.error
from logger import get_logger

logger = get_logger(__name__)


class UrllibHandler:

    def __init__(self, proxies=[]):
        self._proxies = proxies

    def get(self, url):
        request = urllib.request.Request(url)
        proxy = self._get_proxy()
        if proxy:
            request.set_proxy(proxy, 'http')
        logger.info("Attempt to do GET request: url=%s, proxy=%s", url, proxy)
        response = urllib.request.urlopen(request)
        logger.info("GET request was successful: url=%s, proxy=%s", url, proxy)
        return response

    def _get_proxy(self):
        if not self._proxies:
            return
        return random.choice(self._proxies)
