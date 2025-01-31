
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, City
from django.utils.safestring import mark_safe
class CityAdmin(admin.ModelAdmin):
    list_display=["name"]
admin.site.register(City,CityAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            form.base_fields.pop("date_joined",None)
            form.base_fields.pop("last_login",None)
            form.base_fields.pop("password",None)
            form.base_fields.pop("is_superuser",None)
            form.base_fields.pop("is_active",None)
            form.base_fields.pop("is_staff",None)
            form.base_fields.pop("user_permissions",None)
            form.base_fields.pop("groups",None)
        return form
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            # Restrict to the current user if not superuser
            queryset = queryset.filter(id=request.user.id)
        return queryset
    
    list_display =[
        "id",
        "username",
        "email",
        "city",
        "address",
    ]

# Register your custom User model and the UserAdmin
admin.site.register(User, CustomUserAdmin)