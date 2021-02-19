from rest_framework import serializers

from blog.models import Blog, User, Comment, Like
from shared.utils import jwt_obtain_token


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    token = serializers.SerializerMethodField()

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        user = data.get('user')

        # if not User.objects.filter(id=user).exists():
        #     raise serializers.ValidationError("User doesn't exists.")

        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")

        if not len(new_password)>7:
            raise serializers.ValidationError("Password should contain minimum 8 digits.")

        if new_password != confirm_password:
            raise serializers.ValidationError("Password didn't match.")

        return data

    def create(self, validated_data, *args, **kwargs):
        user = validated_data.get('user')
        user.set_password(validated_data['new_password'])
        user.save()

        return user

    def get_token(self, obj):
        return jwt_obtain_token(obj)


class BlogShortSeializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'content')


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'user', 'content')


class BlogReadSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return Like.objects.filter(blog=obj).count()

    def get_comments(self, obj):
        return Comment.objects.filter(blog=obj).count()

    class Meta:
        model = Blog
        fields = ('id', 'user', 'content', 'likes', 'comments')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'user', 'blog', 'content')


class CommentReadSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    blog = BlogShortSeializer()
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return Comment.objects.filter(blog=obj.blog).count()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'blog', 'content', 'comments')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'user', 'blog')
