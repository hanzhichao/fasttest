from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html

from app.models.user import UserProfile

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['avatar', 'username', 'name', 'gender', 'email', 'joined_groups', 'is_active', 'is_staff',
                    'last_login']
    list_display_links = ['username']
    search_fields = ['username']

    filter_horizontal = ['groups', 'user_permissions']
    readonly_fields = ['date_joined', 'last_login']
    autocomplete_fields = ['groups']

    fieldsets = [
        (
            None,
            {
                "fields": ('username',
                           ('last_name', 'first_name'),
                           'email',
                           ('is_active', 'is_staff', 'is_superuser'))
            },
        ),
        (
            "其他",
            {
                "classes": ["collapse"],
                "fields": ['groups',
                           'user_permissions',
                           ('date_joined', 'last_login')],
            },
        ),
    ]

    @admin.display(description='姓名')
    def name(self, obj):
        if obj.first_name:
            if obj.last_name:
                return f'{obj.last_name}{obj.first_name}'
            return obj.first_name

    @admin.display(description='性别')
    def gender(self, obj):
        if obj.profile:
            return obj.profile.get_gender_display()

    @admin.display(description='所属组')
    def joined_groups(self, obj):
        if obj.groups.count() > 0:
            return ', '.join([group.name for group in obj.groups.all()])

    @admin.display(description='头像')
    def avatar(self, obj):
        if obj.profile and obj.profile.avatar:
            avatar = obj.profile.avatar
            return format_html('<img src="{url}" width="{width}" height={height} />'.format(
                url=avatar.url,
                width=24,
                height=24,
            ))

    inlines = [UserProfileInline]
