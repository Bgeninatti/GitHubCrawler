import argparse
import json
import random
import urllib.error

from crawler.crawler import GitHubSearchCrawler, GitHubRepoStatsCrawler
from crawler.http_handler import UrllibHandler, get_urls_async
from crawler.cfg import BASE_URL, SEARCH_URI
from pprint import pprint
from logger import get_logger

logger = get_logger(__name__)

parser = argparse.ArgumentParser(
    description="Get results of a search in github for a certain type of result " + \
                "(wikis, issues or repositories)")
parser.add_argument('-i', '--input', dest="input_file", required=True,
                    help='Path to a json file with the required arguments')
parser.add_argument('-o', '--output', dest="output_file",
                    help='Path where the result will be saved. If is not provided ' + \
                         'we print the result in the stdout')

def main():
    # Parse arguments
    args = vars(parser.parse_args())
    with open(args['input_file'], encoding="utf-8") as jsonfile:
        kwargs = json.loads(jsonfile.read())

    result_type = kwargs['type'].lower()
    keywords = kwargs['keywords']
    proxies = kwargs.get('proxies', [])
    proxy = random.choice(proxies) if proxies else None


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
    gh_crawler = GitHubSearchCrawler(
        search_request.url,
        search_response,
        result_type
    )
    result = gh_crawler.get_result()

    # If results are repos, make aditional requests and search for language statistics & owner
    if result_type == 'repositories':
        responses = get_urls_async([r['url'] for r in result], proxy)
        new_result = []
        for url, response in responses.items():
            if response:
                crawler = GitHubRepoStatsCrawler(url, response)
                extra_data = crawler.get_result()
            else:
                extra_data = None
            new_result.append({'url': url, 'extra': extra_data})
        result = new_result

    # If output file was specified save the result in a file, otherwise print stdout
    output_file = args.get('output_file')
    if output_file:
        json.dump(result, open(output_file, 'w'))
    else:
        print("")
        pprint(result)

if __name__ == '__main__':
    main()
