from rest_framework import serializers
from post.models import Comment, Post
from datetime import datetime

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post   # ← matches your photo (you can change to Comment)
        fields = ['id', 'name', 'body', 'date_added']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['date_added'] = datetime.strftime(
            instance.date_added, '%b %d %Y'
        )
        return rep

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(
        many=True,
        read_only=True,
        source='comment_set'   # ← links to related_name above
    )

    class Meta:
        model  = Post
        fields = ['id', 'title', 'content', 'date_posted','comments']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['date_posted'] = datetime.strftime(
            instance.date_posted, '%b %d %Y'
        )
        rep['comment_count'] = Comment.objects.filter(
            post=instance
        ).count()
        # rep['comments'] = [comment for comment in
        #     Comment.objects.filter(post=instance).values()]
        return rep