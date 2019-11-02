from django.db import models
from django.contrib.auth.models import AbstractUser

from shared.models import BaseModel
from shared.managers import UserManager, BlogManager, CommentManager, LikeManager


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return '{}'.format(self.email)


class Blog(BaseModel):
    '''
    Model to save blog data.
    '''
    user = models.ForeignKey(
        User,
        related_name='user_blog',
        on_delete=models.CASCADE,
        help_text='User related to the blog.')
    content = models.TextField()

    objects = BlogManager()

    class Meta:
        verbose_name = 'Blog'

    def __str__(self):
        return '{}'.format(self.content)


class Comment(BaseModel):
    '''
    '''

    user = models.ForeignKey(
        User,
        related_name='comment',
        on_delete=models.CASCADE,
        help_text='User related to the comment.')
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='blog_comment',
        help_text='Blog related to the comment.')
    content = models.TextField()

    class Meta:
        verbose_name = 'Comment'

    objects = CommentManager()

    def __str__(self):
        return '{}: {}'.format(self.blog, self.content)


class Like(BaseModel):
    '''
    '''

    user = models.ForeignKey(
        User,
        related_name='like',
        on_delete=models.CASCADE,
        help_text='User related to the like.')
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='blog_like',
        help_text='Blog related to the like.')

    class Meta:
        verbose_name = 'Like'

    objects = LikeManager()

    def __str__(self):
        return '{}: {}'.format(self.user, self.blog)
