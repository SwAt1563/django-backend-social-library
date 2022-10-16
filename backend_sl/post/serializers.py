from rest_framework import serializers
from .models import Post, Comment, Star
from account.models import UserAccount
from rest_framework.validators import ValidationError


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
        try:
            post_slug = validated_data.pop('post', '')
            post = Post.objects.get(slug=post_slug)
            user_id = validated_data.pop('user', 0)
            user = UserAccount.objects.get(pk=user_id)
            validated_data = {'user': user, 'post': post}
        except (Post.DoesNotExist, UserAccount.DoesNotExist):
            raise ValidationError('object not exists')
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField(read_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)
    profile_slug = serializers.SerializerMethodField(read_only=True)

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
        return comment.user.get_full_name

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
        try:
            post_slug = validated_data.pop('post', '')
            post = Post.objects.filter(slug=post_slug).first()
            user_id = validated_data.pop('user', 0)
            user = UserAccount.objects.filter(pk=user_id).first()
            comment = validated_data.pop('comment', '')
            validated_data = {'user': user, 'post': post, 'comment': comment}
        except (Post.DoesNotExist, UserAccount.DoesNotExist):
            raise ValidationError('object not exists')
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post:post_review', lookup_field='slug')
    total_stars = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    posted_by = serializers.SerializerMethodField(read_only=True)
    user_image = serializers.SerializerMethodField(read_only=True)
    profile_slug = serializers.SerializerMethodField(read_only=True)
    total_comments = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    user_email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        exclude = ('id', 'user')

    def get_total_stars(self, post):
        return post.get_post_stars_count

    def get_username(self, post):
        return post.user.username

    def get_user_email(self, post):
        return post.user.email

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
    user_id = serializers.CharField(source='user')

    class Meta:
        model = Post
        fields = ('title', 'description', 'file', 'user_id')

    def create(self, validated_data):
        user_id = validated_data.pop('user', 0)
        try:
            user = UserAccount.objects.get(pk=user_id)
            validated_data['user'] = user
        except UserAccount.DoesNotExist:
            raise ValidationError('The user not exists')
        return super().create(validated_data)
