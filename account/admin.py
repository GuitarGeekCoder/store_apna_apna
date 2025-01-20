
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, City

class CityAdmin(admin.ModelAdmin):
    list_display=["name"]
admin.site.register(City,CityAdmin)

class UserAdmin(UserAdmin):
    # Define the fields to be shown in the form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('city',)}),  # Add 'city' field to the user form
    )
    # Optionally, you can add the 'city' field to the list_display
    list_display = UserAdmin.list_display + ('city',)
    # Optionally, add the 'city' field to the add form as well
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('city',)}),
    )

# Register your custom User model and the UserAdmin
admin.site.register(User, UserAdmin)