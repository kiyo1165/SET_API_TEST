from rest_framework import serializers
from core.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('id', 'text', 'tweet_by')
        read_only_fields = ('id',)
