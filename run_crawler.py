import argparse
from crawler.crawler import run_crawler


parser = argparse.ArgumentParser(
    description="Get results of a search in github for a certain type of result " + \
                "(wikis, issues or repositories)")
parser.add_argument('-i', '--input', dest="input_file", required=True,
                    help='Path to a json file with the required arguments')
parser.add_argument('-o', '--output', dest="output_file",
                    help='Path where the result will be saved. If is not provided ' + \
                         'we print the result in the stdout')

if __name__ == '__main__':
    run_crawler(parser)
