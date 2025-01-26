from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "username",
#                     "password1",
#                     "password2",
#                     "email",
#                     "first_name",
#                     "last_name",
#                     "role",
#                 ),
#             },
#         ),
#     )


class CustomUserAdmin(BaseUserAdmin):
    # Display these fields in the admin user list view
    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    list_filter = ("role", "is_staff", "is_active")

    # Add custom fields to the admin form view
    fieldsets = BaseUserAdmin.fieldsets + (("Custom Fields", {"fields": ("role",)}),)

    # Add custom fields to the add user form
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("role",)}),
    )

    # Allow searching by these fields
    search_fields = ("username", "email", "role")

    # Specify ordering
    ordering = ("username",)


# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
