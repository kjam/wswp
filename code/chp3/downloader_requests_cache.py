from random import choice
import requests
import requests_cache

from chp1.throttle import Throttle


class Downloader:
    """ Downloader class to use cache and requests for downloading pages.
        For contructor, pass:
            delay (int): # of secs delay between requests (default: 5)
            user_agent (str): user agent string (default: 'wswp')
            proxies (list[dict]): list of possible proxies, each
                must be a dict with http / https keys and proxy values
            timeout (float/int): number of seconds to wait until timeout
    """
    def __init__(self, delay=5, user_agent='wswp', proxies=None,
                 timeout=60):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = None  # we will set this per request
        self.timeout = timeout

    def __call__(self, url, num_retries=2):
        """ Call the downloader class, which will return HTML from cache
            or download it
            args:
                url (str): url to download
            kwargs:
                num_retries (int): # times to retry if 5xx code (default: 2)
        """
        self.num_retries = num_retries
        proxies = choice(self.proxies) if self.proxies else None
        headers = {'User-Agent': self.user_agent}
        result = self.download(url, headers, proxies)
        return result['html']

    def make_throttle_hook(self, throttle=None):
        """
        Modified from: https://requests-cache.readthedocs.io/en/latest/user_guide.html
        Returns a response hook function which sleeps for `timeout` seconds if
        response is not cached
        """
        def hook(response, *args, **kwargs):
            """ see requests hook documentation for more information"""
            if not getattr(response, 'from_cache', False):
                throttle.wait(response.url)
                print('Downloading:', response.url)
            else:
                print('Returning from cache:', response.url)
            return response
        return hook

    def download(self, url, headers, proxies):
        """ Download a and return the page content
            args:
                url (str): URL
                headers (dict): dict of headers (like user_agent)
                proxies (dict): proxy dict w/ keys 'http'/'https', values
                    are strs (i.e. 'http(s)://IP') (default: None)
        """
        session = requests_cache.CachedSession()
        session.hooks = {'response': self.make_throttle_hook(self.throttle)}

        try:
            resp = session.get(url, headers=headers, proxies=proxies,
                               timeout=self.timeout)
            html = resp.text
            if resp.status_code >= 400:
                print('Download error:', resp.text)
                html = None
                if self.num_retries and 500 <= resp.status_code < 600:
                    # recursively retry 5xx HTTP errors
                    self.num_retries -= 1
                    return self.download(url, headers, proxies)
        except requests.exceptions.RequestException as e:
            print('Download error:', e)
            return {'html': None, 'code': 500}
        return {'html': html, 'code': resp.status_code}
