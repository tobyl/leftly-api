from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False)
    class Meta:
        model = Post
        fields = (
            'slug',
            'created',
            'url',
            'type',
            'body',
            'tweet_owner',
            'tweet_id',
            'tweet_body',
            'video_id',
            'tweet_owner',
            'tweet_id',
            'tweet_created',
            'tweet_owner_avatar',
        )

