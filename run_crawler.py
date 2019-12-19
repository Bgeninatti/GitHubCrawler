import argparse
import json
import sys
from crawler import GitHubSearchCrawler, HTTPHandler

parser = argparse.ArgumentParser(
    description="Get results of a search in github for a certain type of result " + \
                "(wikis, issues or repositories)")
parser.add_argument('--file', metavar='--file', dest="input_file",
                    help='Path to a json file with the required arguments')

def main():
    args = vars(parser.parse_args())
    with open(args['input_file'], encoding="utf-8") as jsonfile:
        kwargs = json.loads(jsonfile.read())
    http_handler = HTTPHandler(kwargs['proxies'])
    gh_crawler = GitHubSearchCrawler(
        '+'.join(kwargs['keywords']),
        kwargs['type'],
        http_handler
    )
    gh_crawler.run()
    sys.stdout.write(json.dumps(gh_crawler.get_result()))

if __name__ == '__main__':
    main()
