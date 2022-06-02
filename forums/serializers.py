from rest_framework import serializers

from forums.models import Post, Category, Comment, Rating
from django.db.models import Avg


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def is_liked(self, post):
        user = self.context.get('request').user
        return user.liked.filter(post=post).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance)
        representation['likes_count'] = instance.likes.count()
        representation['rating'] = instance.ratings.aggregate(Avg('mark'))
        representation['comments_detail'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation

    class Meta:
        model = Post
        fields = ('name', 'owner', 'category', 'body', 'image', 'comments', 'ratings')


class PostListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.ratings.aggregate(Avg('mark'))
        return representation

    class Meta:
        model = Post
        fields = ('name', 'owner', 'category', 'image', 'ratings')


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['posts'] = PostListSerializer(instance.products.all(), many=True).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    # post = serializers.ReadOnlyField(source='post.name')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'post')


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Rating
        fields = '__all__'
