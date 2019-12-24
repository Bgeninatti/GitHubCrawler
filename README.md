# GitHub Crawler
 
GitHub Crawler that implements the GitHub search. Return all the links in the first page of results.

Search types supported:

* Wikis
* Issues
* Repositories

## Usage
### 1. Insall dependencies:
  ```
  $ pip install -r requirements.txt
  ```
### 2. Set your input
  
  Add your input parameters in a JSON file, or use one of the two sample files provided: 
  [sample_input.json](https://github.com/Bgeninatti/GitHubCrawler/blob/master/sample_input.json),
  [sample_input_no_proxies.json](https://github.com/Bgeninatti/GitHubCrawler/blob/master/sample_input_no_proxies.json)
  
  The JSON file should contain something like:
  
  ```json
  {
  "keywords": [
    "openstack",
    "nova",
    "css"
  ],
  "proxies": [
    "194.126.37.94:8080",
    "13.78.125.167:8080"
  ],
  "type": "Repositories"
  }
  ```
  **NOTES:** 
  
  * The `proxies` argument is optional, `keyword` and `type` are required 
  * `type` can be one of the three types supported (is not case-sensitive): *Repositories*, *Wikis* and *Issues*  

### 3. Run the crawler:
  ```bash
  $ python3 run_crawler.py -i input.json
  ```
  
  Optionally you can provide the `-o` or `--output` argument to save the crawler result in a json file. 
  If this argument is not provided the result will be displayed in stdout.
  ```bash
  $ python3 run_crawler.py -i input.json -o output.json
  ```
  
  And you always can ask for help :)
  ```
  $ python3 run_crawler.py -h
  usage: run_crawler.py [-h] -i INPUT_FILE [-o OUTPUT_FILE]

Get results of a search in github for a certain type of result (wikis, issues
or repositories)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input INPUT_FILE
                        Path to a json file with the required arguments
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Path where the result will be saved. If is not
                        provided we print the result in the stdout

  ```
  
  ## Tests and coverage
  
  Dependencies in `requirements.txt` also install the packages for tests and test coverage.
  To run the tests and check the test coverage run:
  
  ```
  $ pytest -v --cov=crawler/ --cov-report html
  ```
  
  The tests result will be displayed in the stdout.
  The tests coverage results can be found in `testcov/index.html`
  
  ### Current coverage
  
Module|Statements|Missing|Excluded|Coverage
------|----------|-------|--------|--------
crawler/\_\_init\_\_.py |	0 |	0 |	0 |	100%
crawler/cfg.py |	3 |	0 |	0 |	100%
crawler/crawler.py |	46 |	14 |	0 |	70%
crawler/http_handler.py |	38 |	1 |	0 |	97%
crawler/parsers.py |	33 |	0 |	0 |	100%
|**Total** |	**120** |	**15** |	**0** |	**88%** |
