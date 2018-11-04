import json, time
from django.db import models
from django.conf import settings
from .constants import POST_TYPE
from .utils import slugify_max, get_tweet_id, tweet_slug
import twitter

api = twitter.Api(
    consumer_key=getattr(settings, 'TWITTER_CONSUMER_KEY', None),
    consumer_secret=getattr(settings, 'TWITTER_CONSUMER_SECRET', None),
    access_token_key=getattr(settings, 'TWITTER_ACCESS_TOKEN_KEY', None),
    access_token_secret=getattr(settings, 'TWITTER_ACCESS_TOKEN_SECRET', None)
)


class PostManager(models.Manager):
    def create(self, *args, **kwargs):
        if 'type' in kwargs and kwargs['type'] == 'post':
            kwargs['slug'] = slugify_max(kwargs['body'])
        #   api.PostUpdate(kwargs['body'])
        if 'type' in kwargs and kwargs['type'] == 'retweet':
            # creating a tweet
            tweet_id = get_tweet_id(kwargs['body'])
            kwargs['slug'] = tweet_slug(tweet_id)
            tweet = api.GetStatus(tweet_id).AsDict()
            try:
                kwargs['tweet_owner'] = tweet.get('user', {}).get('screen_name')
                kwargs['tweet_owner_name'] = tweet.get('user', {}).get('name')
                kwargs['tweet_id'] = tweet.get('id', None)
                kwargs['tweet_body'] = tweet.get('text', None)
                kwargs['tweet_owner_avatar'] = tweet.get('user', {}).get('profile_image_url_https')
                kwargs['tweet_created'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.strptime(tweet.get('created_at', None), '%a %b %d %H:%M:%S +0000 %Y'))
            except Exception:
                print('Retweet could not be created')

        return super().create(**kwargs)


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=POST_TYPE, default='Post', blank=False, null=False)
    body = models.TextField(max_length=400)
    slug = models.SlugField(max_length=50, unique=True, primary_key=True)

    # for retweets

    tweet_owner = models.CharField(max_length=100, blank=True, null=True)
    tweet_owner_name = models.CharField(max_length=100, blank=True, null=True)
    tweet_id = models.BigIntegerField(blank=True, null=True)
    tweet_body = models.TextField(max_length=400, blank=True, null=True)
    tweet_owner_avatar = models.URLField(blank=True, null=True)
    tweet_created = models.CharField(max_length=60, blank=True, null=True)

    # for videos

    video_id = models.CharField(max_length=100, blank=True, null=True)

    objects = PostManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.slug
