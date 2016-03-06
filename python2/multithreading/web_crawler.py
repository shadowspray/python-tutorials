# -*- coding: utf-8 -*-
import logging
import re
import threading
import Queue
import sys

import concurrent.futures
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

html_link_regex = re.compile('<a\s(?:.*?\s)*?href=[\'"](.*?)[\'"].*?>')
urls = Queue.Queue()
urls.put('http://www.google.com')
urls.put('http://br.bing.com/')
urls.put('https://duckduckgo.com/')
urls.put('https://github.com/')
urls.put('http://br.search.yahoo.com/')

result_dict = {}


def group_urls_task(urls):
    try:
        url = urls.get(True, 0.05)
        result_dict[url] = None
        logger.info('[%s] putting url [%s] in dictionary...' % (
            threading.current_thread().name, url))
    except Queue.Empty:
        logging.error('Nothing to be done, queue is empty')
    finally:
        logging.info('Queue size now: %s' % urls.qsize())


def crawl_task(url):
    links = []
    try:
        request_data = requests.get(url)
        logger.info('[%s] crawling url [%s] ...' % (
            threading.current_thread().name, url))
        links = html_link_regex.findall(request_data.text)
    except:
        logger.error(sys.exc_info()[0])
        raise
    finally:
        return url, links


logger.info('Queue size at the beginning: %s' % urls.qsize())

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as group_link_threads:
    for i in range(urls.qsize()):
        group_link_threads.submit(group_urls_task, urls)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as crawler_link_threads:
    future_tasks = {crawler_link_threads.submit(crawl_task, url): url for url in result_dict.keys()}
    for future in concurrent.futures.as_completed(future_tasks):
        url = future_tasks[future]
        result_dict[url] = future.result()
    for k, v in result_dict.iteritems():
        logger.info('Crawler results: %s - %s' % (k, v))
