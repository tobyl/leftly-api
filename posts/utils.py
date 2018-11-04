import re, datetime
from django.template.defaultfilters import slugify

def slugify_max(text, max_length=50):
    slug = slugify(text)
    if len(slug) <= max_length:
        return slug
    trimmed_slug = slug[:max_length].rsplit('-', 1)[0]
    if len(trimmed_slug) <= max_length:
        return trimmed_slug
    # First word is > max_length chars, so we have to break it
    return slug[:max_length]

def get_tweet_owner(url):
    tweet_regex = re.search('https?://(.*\.)?twitter\.com\/([A-z 0-9 _]+)\/?', url)
    return tweet_regex.group(2)

def get_tweet_id(url):
    tweet_id = re.search('/status/(\d+)', url)
    return tweet_id.group(1)

def tweet_slug(tweet_id):
    now = datetime.datetime.now()
    return "{}-{}-{}-{}".format(now.year, now.month, now.day, tweet_id)
