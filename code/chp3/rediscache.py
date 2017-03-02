import json
import zlib
from datetime import datetime, timedelta
from redis import StrictRedis


class RedisCache:
    """ RedisCache helps store urls and their responses to Redis
        Initialization components:
            client: a Redis client connected to the key-value database for
                the webcrawling cache (if not set, a localhost:6379
                default connection is used).
            expires (datetime.timedelta): timedelta when content will expire
                (default: 30 days ago)
            encoding (str): character encoding for serialization
            compress (bool): boolean indicating whether compression with zlib should be used
    """
    def __init__(self, client=None, expires=timedelta(days=30), encoding='utf-8', compress=True):
        self.client = (StrictRedis(host='localhost', port=6379, db=0)
                       if client is None else client)
        self.expires = expires
        self.encoding = encoding
        self.compress = compress

    def __getitem__(self, url):
        """Load data from Redis for given URL"""
        record = self.client.get(url)
        if record:
            if self.compress:
                record = zlib.decompress(record)
            return json.loads(record.decode(self.encoding))
        else:
            # URL has not yet been cached
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """Save data to Redis for given url"""
        data = bytes(json.dumps(result), self.encoding)
        if self.compress:
            data = zlib.compress(data)
        self.client.setex(url, self.expires, data)
