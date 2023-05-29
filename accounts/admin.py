from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.site_header = 'EMCS'
admin.site.site_title = 'EMCS Portal'
admin.site.index_title = 'EMCS Backend'

class MyUser(BaseUserAdmin):
    
    ordering = ['-username']
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active']
    list_display_links = ['email', 'username']
    list_filter = ['email', 'username', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_login', 'date_joined']
    readonly_fields = ['date_joined', 'last_login']
    filter_horizontal = ()
    fieldsets = (
        (
            _('Login Credentials'),
            {
                'fields': ('email', 'password',) 
            },
        ),
        (
            _('Personal Information'),
            {
                'fields': ('username', 'first_name', 'last_name',)
            },
        ),
        (
            _('Permissions and Groups'),
            {
                'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')
            }

        ),

        (
            _('Date Joined and Last Login'),
            {
                'fields': ('date_joined', 'last_login')
            }

        ),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields' : ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

admin.site.register(User, MyUser)