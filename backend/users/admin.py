from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = ('username', 'email', 'last_name')
    list_filter = ['username', 'email', 'first_name', 'last_name']


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'following'
    )
    list_filter = ['user', 'following']


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
