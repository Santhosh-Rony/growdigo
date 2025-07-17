from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'payment_status', 'payment_amount', 'is_staff', 'is_active',)
    list_filter = ('payment_status', 'is_staff', 'is_active', 'payment_date')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Payment info', {'fields': ('payment_status', 'payment_amount', 'payment_date', 'razorpay_payment_id', 'razorpay_order_id')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'name',)
    ordering = ('email',)
    readonly_fields = ('payment_date',) 