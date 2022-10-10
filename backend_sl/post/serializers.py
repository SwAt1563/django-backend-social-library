from rest_framework import serializers
from .models import Post, Comment, Star

class StarSerializer(serializers.ModelSerializer):
    post_slug = serializers.SlugField()
    class Meta:
        model = Star
        fields = ('user', 'post_slug')

    def create(self, validated_data):
        post_slug = validated_data.get('post_slug', '')
        post = Post.objects.filter(slug=post_slug)
        user = validated_data.get('user', None)
        print(user, post)
        star = Star(post__id=post.id, user__id=user.id)
        print(star)
        return star


class CommentSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('comment', 'created', 'user_image', 'user_name')

    def get_user_image(self, comment):
        if comment.user.profile.image:
            request = self.context.get('request')
            photo_url = comment.user.profile.image.url
            return request.build_absolute_uri(photo_url)
        return None

    def get_user_name(self, comment):
        first_name = comment.user.first_name
        last_name = comment.user.last_name
        return str(first_name) + ' ' + str(last_name)

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post:post_detail', lookup_field='slug')
    total_stars = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    user_name = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ('id', 'user')

    def get_total_stars(self, post):
        return post.stars.count()

    def get_user_name(self, post):
        first_name = post.user.first_name
        last_name = post.user.last_name
        return str(first_name) + ' ' + str(last_name)

    def get_user_image(self, post):
        if post.user.profile.image:
            request = self.context.get('request')
            photo_url = post.user.profile.image.url
            return request.build_absolute_uri(photo_url)
        return None