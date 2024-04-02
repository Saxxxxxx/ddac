from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import User
from django.utils.html import format_html

User = get_user_model()

def make_users_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

make_users_active.short_description = _("Make selected users active")

def ban_users(modeladmin, request, queryset):
    queryset.update(is_banned=True)
ban_users.short_description = _("Ban selected users")

class IsBannedFilter(admin.SimpleListFilter):
    title = _('Is Banned')
    parameter_name = 'is_banned'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_banned=True)
        elif self.value() == 'no':
            return queryset.filter(is_banned=False)
        return queryset

class UserAdmin(UserAdmin):
    '''DEFINE ADMIN MODEL FOR CUSTOM USER MODEL WITH NO USERNAME FIELD'''
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','avatar_tag','avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_banned'),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_banned')
    search_fields = ('email', 'first_name', 'last_name', 'is_active')
    ordering = ('email',)
    readonly_fields = ('avatar_tag',)
    list_filter = ('groups','is_active', 'is_staff', 'is_superuser', IsBannedFilter)
    actions = [make_users_active,ban_users]

    def avatar_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.avatar.url))
    avatar_tag.short_description = "Avatar Thumbnail"


    
admin.site.register(User, UserAdmin)