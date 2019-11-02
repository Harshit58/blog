from django.contrib import admin

from blog.models import User, Blog, Comment, Like
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    list_display = ('id', 'email')
    ordering = ('email', )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Permissions'), {'fields': ('is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blog', 'content')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blog')


admin.site.register(User, UserAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
