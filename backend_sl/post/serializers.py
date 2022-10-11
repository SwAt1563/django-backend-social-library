from rest_framework import serializers
from .models import Post, Comment, Star
from account.models import UserAccount


# you should send post_slug and user_id of the user who want to make star or that post for make a new star
# the user can just make one star for each post
class StarCreateSerializer(serializers.ModelSerializer):
    post_slug = serializers.SlugField(source='post')
    user_id = serializers.CharField(source='user')

    # the required fields should be included
    # so instead for send post and user i wanna send post_slug and user_id
    # then i changed the fields and point the the original fields
    # and handle that in create method
    class Meta:
        model = Star
        fields = ('post_slug', 'user_id')

    def create(self, validated_data):
        post_slug = validated_data.pop('post', '')
        post = Post.objects.filter(slug=post_slug).first()
        user_id = validated_data.pop('user', 0)
        user = UserAccount.objects.filter(pk=user_id).first()
        validated_data = {'user': user, 'post': post}
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    profile_slug = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('comment', 'created', 'user_image', 'user_name', 'profile_slug')

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

    def get_profile_slug(self, comment):
        if comment.user.profile:
            profile_slug = comment.user.profile.slug
            return profile_slug
        return None

# you should send user_id of the user who commented and the comment and the post_slug
class CommentCreateSerializer(serializers.ModelSerializer):
    post_slug = serializers.SlugField(source='post')
    user_id = serializers.CharField(source='user')

    class Meta:
        model = Comment
        fields = ('user_id', 'post_slug', 'comment')

    def create(self, validated_data):
        post_slug = validated_data.pop('post', '')
        post = Post.objects.filter(slug=post_slug).first()
        user_id = validated_data.pop('user', 0)
        user = UserAccount.objects.filter(pk=user_id).first()
        comment = validated_data.pop('comment', '')
        validated_data = {'user': user, 'post': post, 'comment': comment}
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post:post_review', lookup_field='slug')
    total_stars = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    posted_by = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    profile_slug = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ('id', 'user')

    def get_total_stars(self, post):
        return post.get_post_stars_count

    def get_total_comments(self, post):
        return post.comments.count()

    def get_posted_by(self, post):
        return post.posted_by

    def get_user_image(self, post):
        if post.user.profile.image:
            request = self.context.get('request')
            photo_url = post.user.profile.image.url
            return request.build_absolute_uri(photo_url)
        return None

    def get_profile_slug(self, post):
        if post.user.profile:
            profile_slug = post.user.profile.slug
            return profile_slug
        return None


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'description', 'file', 'user')
