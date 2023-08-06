import json
import urllib.request

import constants


def open(url):
    for char in url:
        if char in constants.URL_CODES:
            url = url.replace(char, constants.URL_CODES[char])
    
    return json.loads(urllib.request.urlopen(url, timeout=constants.DEFAULT_TIMEOUT).read().decode("utf-8"))
