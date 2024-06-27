#!/usr/bin/env python

import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

EXTENSIONS = [
    'pdf', 'doc', 'docx', 'rtf', 'env', 'bak', 'sql', 'ppt', 'pps', 'pptx', 'ppsx',
    'xls', 'xlsx', 'sxw', 'sxc', 'sxi', 'odt', 'ods', 'odg', 'odp', 'wpd', 'indd',
    'rdp', 'ica', 'rar', 'txt', 'xml', '7z', 'zipx'
]

def make_search_query(domain, extensions):
    params = ' OR '.join(map(lambda extension: 'filetype:' + extension, extensions))
    if len(extensions) > 1:
        params = '(' + params + ')'
    return f'site:{domain} {params}'

def parse_google_serp(query):
    primary_url = f'https://www.google.com/search?num=100&start=0&hl=en&meta=&q={query}&filter=0'

    print('\nInitializing Chrome...')
    print(f'\nOpening {primary_url}')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_argument('user-data-dir=/home/mikel/.config/BraveSoftware/Brave-Browser/Library/Application Support/Google/Chrome')
    browser = webdriver.Chrome(options=chrome_options)

    browser.get(primary_url)

    # Use explicit wait to check for the CAPTCHA form
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#captcha-form')))
        sys.exit('\nError: captcha detected. Solve captcha and run script again.')
    except TimeoutException:
        pass

    results = parse_google_serp_single_page(browser)
    print(f'\nFound {len(results)} files in Google. Waiting...')

    # Find pagination links
    pages = [page.get_attribute('href') for page in browser.find_elements(By.CSS_SELECTOR, '#nav td a.fl')]
    if pages:
        print(f'Detected {len(pages)} additional search results pages')
        for page in pages:
            browser.get(page)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.r > a')))
            page_results = parse_google_serp_single_page(browser)
            print(f'Found {len(page_results)} more files in Google. Waiting...')
            results.extend(page_results)

    browser.quit()
    return results

def parse_google_serp_single_page(browser):
    anchor_elements = browser.find_elements(By.TAG_NAME,'a')
    links = [anchor.get_attribute('href') for anchor in anchor_elements if anchor.get_attribute('href') is not None]
    return links

def save_log_file(results, domain, filename):
    filepath = f'{domain}/{filename}'
    os.makedirs(domain, exist_ok=True)
    with open(filepath, 'w') as file:
        file.write('\n'.join(results))
    print(f'Saved results to {filepath} ({len(results)} files total)')


def download_files(results, domain, filename):
    print(f'\n\n\nDownloading {len(results)} files from {domain}/{filename} into {domain} folder...\n\n\n')
    with open(f'./{domain}/{filename}', 'r') as file:
        links = file.readlines()
    
    filtered_links = [link.strip() for link in links if domain in link]

    temp_filename = f'./{domain}/temp_log.txt'
    with open(temp_filename, 'w') as temp_file:
        temp_file.write('\n'.join(filtered_links))
    
    os.system(f'wget -i {temp_filename} -P ./{domain}')
    
    os.remove(temp_filename)
    
    print(f'\n\n\nSuccessfully downloaded {len(filtered_links)} files into {domain} folder\n\n\n')

def init_csv_search():
    print(f'\nSearching public repositories on {domain}...')
    query = make_search_query(domain, ['git', 'svn'])
    repositories = parse_google_serp(query)
    save_log_file(repositories, domain, '0_repositories.txt')

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
        if extension == '--cvs':
            init_csv_search()
            sys.exit()
        else:
            query = make_search_query(domain, [extension])
    else:
        query = make_search_query(domain, EXTENSIONS)

    os.makedirs(domain, exist_ok=True)

    print(f'\nSearching {"all static" if not extension else extension.upper()} files on {domain}')
    results = parse_google_serp(query)
    save_log_file(results, domain, '0_log.txt')
    download_files(results, domain, '0_log.txt')
