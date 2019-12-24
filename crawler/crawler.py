import json
import random
import urllib.error
from pprint import pprint

from crawler.parsers import GitHubSearchParser, GitHubRepoStatsParser
from crawler.http_handler import UrllibHandler, get_urls_async
from crawler.cfg import BASE_URL, SEARCH_URI
from logger import get_logger

logger = get_logger(__name__)


def get_repositories_data(urls, proxy):
    """
    Get owner and languages statistics from all the repose
    in `urls`
    """
    responses = get_urls_async(urls, proxy)
    result = []
    for url, response in responses.items():
        parser = GitHubRepoStatsParser(response)
        extra_data = parser.get_result()
        result.append({'url': url, 'extra': extra_data})
    return result


def do_github_search(keywords, result_type, proxy):
    """
    Perform a search in GitHub for the given keywords and result type.
    If proxy is None, no proxy will be used.
    Returns a list of dicts with urls of results in first page.
    """
    # Perform search request
    search_request = UrllibHandler(f"{BASE_URL}{SEARCH_URI}",
                                   proxy,
                                   q='+'.join(keywords),
                                   type=result_type)
    try:
        search_response = search_request.get()
    except (urllib.error.URLError, urllib.error.HTTPError) as ex:
        logger.error("Unexpected error during search request: url=%s, proxy=%s, " + \
                     "error=%s", search_request.url, proxy, ex)
        return

    # Search result in HTML tree
    search_parser = GitHubSearchParser(
        search_response,
        result_type
    )
    result = search_parser.get_result()
    return result


def parse_input_file(input_filename):
    """
    Read `input_file` as a json and return a list of keywords, result_type
    and proxies list (or empty list of not present int JSON)
    """
    with open(input_filename, encoding="utf-8") as jsonfile:
        kwargs = json.loads(jsonfile.read())

    result_type = kwargs['type'].lower()
    keywords = kwargs['keywords']
    proxies = kwargs.get('proxies', [])
    return keywords, result_type, proxies


def run_crawler(parser):
    """
    Run the GitHub crawler for a given JSON file with input params
    """
    # Parse arguments
    args = vars(parser.parse_args())
    keywords, result_type, proxies = parse_input_file(args['input_file'])
    proxy = random.choice(proxies) if proxies else None
    result = do_github_search(keywords, result_type, proxy)

    # If results are repos, make aditional requests and search for language statistics & owner
    if result_type == 'repositories':
        result = get_repositories_data([r['url'] for r in result], proxy)

    # If output file was specified save the result in a file, otherwise print stdout
    output_file = args.get('output_file')
    if output_file:
        json.dump(result, open(output_file, 'w'))
    else:
        print("")
        pprint(result)

