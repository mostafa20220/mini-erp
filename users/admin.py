from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Business", {
            "fields": (
                'customer_code',
                'phone',
                'address',
                'opening_balance',
                'role',
            )
        }),
        ("Audit", {
            "fields": (
                'created_by',
                'modified_by',
                'created_at',
                'modified_at',
            )
        }),
    )

    list_display = ( 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active','modified_by','created_by','modified_at','created_at')

    readonly_fields = (
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
    )
    search_fields = ('email', 'id','phone')
    list_filter = ('is_staff', 'is_active', 'role',)
    ordering = ('-id',)