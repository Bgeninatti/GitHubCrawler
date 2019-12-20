import argparse
import json
import sys
from crawler.crawler import GitHubSearchCrawler
from crawler.http_handler import UrllibHandler
from pprint import pprint

parser = argparse.ArgumentParser(
    description="Get results of a search in github for a certain type of result " + \
                "(wikis, issues or repositories)")
parser.add_argument('-i', '--input', dest="input_file", required=True,
                    help='Path to a json file with the required arguments')
parser.add_argument('-o', '--output', dest="output_file",
                    help='Path where the result will be saved. If is not provided ' + \
                         'we print the result in the stdout')

def main():
    args = vars(parser.parse_args())
    with open(args['input_file'], encoding="utf-8") as jsonfile:
        kwargs = json.loads(jsonfile.read())
    http_handler = UrllibHandler(kwargs.get('proxies', []))
    gh_crawler = GitHubSearchCrawler(
        '+'.join(kwargs['keywords']),
        kwargs['type'],
        http_handler
    )
    gh_crawler.run()
    output_file = args.get('output_file')
    result = gh_crawler.get_result()
    if output_file:
        json.dump(result, open(output_file, 'w'))
    else:
        print("")
        pprint(result)

if __name__ == '__main__':
    main()
