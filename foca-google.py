#!/usr/bin/env python

import time
import sys
import os
import re
from selenium import webdriver


FIND_AND_DOWNLOAD = [
    'pdf',
    'doc',
    'docx',
    'rtf',
    'ppt',
    'pps',
    'pptx',
    'ppsx',
    'xls',
    'xlsx',
    'sxw',
    'sxc',
    'sxi',
    'odt',
    'ods',
    'odg',
    'odp',
    'wpd',
    'indd',
    'rdp',
    'ica',
    'rar',
    'txt',
    'xml',
    '7z',
    'zipx'
];

FIND_URLS_ONLY = [
    'git',
    'svn'
]


def make_search_query(domain, extensions):
    params = ' OR '.join(map(lambda extension : 'filetype:' + extension, extensions))
    if len(extensions) > 1:
        params = '(' + params + ')'
    return 'site:{0} {1}'.format(domain, params)


def parse_google_serp(query):
    primary_url = 'https://www.google.com/search?num=100&start=0&hl=em&meta=&q={0}&filter=0'.format(query)

    print('\nInitializing Chrome...');
    print('\nOpening ' + primary_url);

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_argument('user-data-dir={0}/Library/Application Support/Google/Chrome'.format(os.path.expanduser('~')))
    browser = webdriver.Chrome(options=chrome_options)

    browser.get(primary_url)
    time.sleep(3)

    is_captcha = len(browser.find_elements_by_css_selector('#captcha-form'))
    if is_captcha:
        sys.exit('\nError: captcha detected. Solve captcha and run script again.')

    results = parse_google_serp_single_page(browser);
    print('\nFound {0} files in Google. Waiting...'.format(len(results)))

    pages = list(map(lambda page : page.get_attribute('href'), browser.find_elements_by_css_selector('#nav td > a.fl')))

    if len(pages):
        print('Detected {0} additional search results pages'.format(len(pages)))
        for page in pages:
            browser.get(page)
            time.sleep(3)
            page_results = parse_google_serp_single_page(browser)
            print('Found {0} more files in Google. Waiting...'.format(len(page_results)))
            results.extend(page_results)

    browser.quit()
    return results;


def parse_google_serp_single_page(browser):
    is_captcha = len(browser.find_elements_by_css_selector('#captcha-form'))
    if is_captcha:
        return [];
    return list(map(lambda res : res.get_attribute('href'), browser.find_elements_by_css_selector('.r > a:not(.fl)')))


def save_log_file(results, domain, filename):
    filepath = '{0}/{1}'.format(domain, filename)
    os.system('touch ./' + filepath)
    file = open(filepath, 'w+')
    file.write('\n'.join(results))
    file.close()
    print('Saved results to {0} ({1} files total)'.format(filepath, len(results)))


def download_files(results, domain, filename):
    print('\n\n\nDownloading {0} files from {1}/{2} into {1} folder...\n\n\n'.format(len(results), domain, filename))
    os.system('wget -i ./{0}/{1} -P ./{0}'.format(domain, filename))
    print('\n\n\nSuccessfully downloaded {0} files into {1} folder\n\n\n'.format(len(results), domain))


if len(sys.argv) == 1:
    print("""
    Format:
    foca-google domain.com [optional-file-extension]

    Usage:
    foca-google example.com         - finds and downloads all possible static files from example.com
    foca-google example.com doc     - finds and downloads only DOC files from example.com
    """)

else:
    domain = sys.argv[1]
    extension = ''

    if len(sys.argv) == 3:
        extension = sys.argv[2]
        query = make_search_query(domain, [extension])
    else:
        query = make_search_query(domain, FIND_AND_DOWNLOAD)

    os.system('mkdir ./{0}'.format(domain))

    print('\nSearching {0} files on {1}'.format('all static' if not extension else extension.upper(), domain))
    results = parse_google_serp(query)
    save_log_file(results, domain, '0_log.txt')

    print ('\nSearching public repositories on {0}...'.format(domain))
    repositories = parse_google_serp(make_search_query(domain, FIND_URLS_ONLY))
    save_log_file(repositories, domain, '0_repositories.txt')

    download_files(results, domain, '0_log.txt')
