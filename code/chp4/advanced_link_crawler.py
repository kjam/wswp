import re
import socket
from urllib import robotparser
from urllib.parse import urljoin, urlparse
from chp3.downloader import Downloader

socket.setdefaulttimeout(60)


def get_robots_parser(robots_url):
    " Return the robots parser object using the robots_url "
    try:
        rp = robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp
    except Exception as e:
        print('Error finding robots_url:', robots_url, e)


def get_links(html):
    " Return a list of links (using simple regex matching) from the html content "
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


def link_crawler(start_url, link_regex, robots_url=None, user_agent='wswp',
                 proxies=None, delay=3, max_depth=4, num_retries=2, cache={}, scraper_callback=None):
    """ Crawl from the given start URL following links matched by link_regex. In the current
        implementation, we do not actually scrapy any information.

        args:
            start_url (str or list of strs): web site(s) to start crawl
            link_regex (str): regex to match for links
        kwargs:
            robots_url (str): url of the site's robots.txt (default: start_url + /robots.txt)
            user_agent (str): user agent (default: wswp)
            proxies (list of dicts): a list of possible dicts for http / https proxies
                For formatting, see the requests library
            delay (int): seconds to throttle between requests to one domain (default: 3)
            max_depth (int): maximum crawl depth (to avoid traps) (default: 4)
            num_retries (int): # of retries when 5xx error (default: 2)
            cache (dict): cache dict with urls as keys and dicts for responses (default: {})
            scraper_callback: function to be called on url and html content
    """
    if isinstance(start_url, list):
        crawl_queue = start_url
    else:
        crawl_queue = [start_url]
    # keep track which URL's have seen before
    seen, robots = {}, {}
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, cache=cache)
    while crawl_queue:
        url = crawl_queue.pop()
        no_robots = False
        if 'http' not in url:
            continue
        domain = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
        rp = robots.get(domain)
        if not rp and domain not in robots:
            robots_url = '{}/robots.txt'.format(domain)
            rp = get_robots_parser(robots_url)
            if not rp:
                # issue finding robots.txt, still crawl
                no_robots = True
            robots[domain] = rp
        elif domain in robots:
            no_robots = True
        # check url passes robots.txt restrictions
        if no_robots or rp.can_fetch(user_agent, url):
            depth = seen.get(url, 0)
            if depth == max_depth:
                print('Skipping %s due to depth' % url)
                continue
            html = D(url, num_retries=num_retries)
            if not html:
                continue
            if scraper_callback:
                links = scraper_callback(url, html) or []
            else:
                links = []
            # filter for links matching our regular expression
            for link in get_links(html) + links:
                if re.match(link_regex, link):
                    if 'http' not in link:
                        if link.startswith('//'):
                            link = '{}:{}'.format(urlparse(url).scheme, link)
                        elif link.startswith('://'):
                            link = '{}{}'.format(urlparse(url).scheme, link)
                        else:
                            link = urljoin(domain, link)

                    if link not in seen:
                        seen[link] = depth + 1
                        crawl_queue.append(link)
        else:
            print('Blocked by robots.txt:', url)


if __name__ == '__main__':
    from chp4.alexa_callback import AlexaCallback
    from chp3.rediscache import RedisCache
    from time import time
    AC = AlexaCallback()
    AC()
    start_time = time()
    link_crawler(AC.urls, '$^', cache=RedisCache())
    print('Total time: %ss' % (time() - start_time))
