import re
import textwrap
import requests
import urllib.parse as parse

QUOTE_PATTERN = re.compile(r'[\"\u201c\u201e\u00ab]\s?(.+?)\s?[\"\u201c\u201d\u00bb]')
LINK_PATTERN = re.compile(r'https?://')


def dedent(string):
    return textwrap.dedent(string).replace('\n', '')


def extract_quotes(string):
    return re.findall(QUOTE_PATTERN, string)


def extract_links(string):
    words = string.split(' ')
    return [word for word in words if re.match(LINK_PATTERN, word)]


def record(keys):
    placeholders = [None for key in keys]
    return dict(zip(keys, placeholders))


def flatten(d, connector='_', skip=[], parent_key=''):
    items = []

    for sub_key, v in d.items():
        if parent_key:
            key = parent_key + connector + sub_key
        else:
            key = sub_key

        if isinstance(v, dict) and not (key in skip):
            items.extend(flatten(v, connector, skip, key).items())
        else:
            items.append((key, v))

    return dict(items)


def resolve(url):
    response = requests.head(url, allow_redirects=True)
    return response.url


def base(url):
    base = parse.urlsplit(url)[:3]
    url = parse.urlunsplit(base + ('', ''))
    return url
