import json
import urllib.request

import utils.constants


def open(url):
    for char in url:
        if char in utils.constants.URL_CODES:
            url = url.replace(char, utils.constants.URL_CODES[char])
    
    return json.loads(urllib.request.urlopen(url, timeout=utils.constants.DEFAULT_TIMEOUT).read().decode("utf-8"))
