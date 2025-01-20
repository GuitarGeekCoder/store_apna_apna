from django.contrib import admin
from .models import Store, Product
from django.contrib import messages
from django.http import HttpResponse
from django.utils.safestring import mark_safe

class StoreAdmin(admin.ModelAdmin):
    # Override the get_form method to conditionally hide the user field
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            form.base_fields.pop("user", None)
            form.base_fields.pop("status", None)
        return form

    def add_view(self, request, form_url="", extra_context=None):
        if not request.user.is_superuser:
            # Get the store of the logged-in user
            store = Store.objects.filter(user=request.user).first()
            if store:
                messages.error(
                    request,
                    "You already have a store. Please do not create another one.",
                )
                return HttpResponse(
                    "You already have a store. Please do not create another one."
                )  # You can customize this message

        # If store is active, proceed with the usual add view
        return super().add_view(request, form_url, extra_context)

    # Automatically assign the logged-in user as the user for the Store
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user  # Automatically assign the logged-in user
            obj.status = "pending_verification"
        super().save_model(request, obj, form, change)

    list_display = (
        "name",
        "gstin",
        "status",
        "category",
    )  # Display user info alongside store
    search_fields = ("name", "gstin", "category")


class ProductAdmin(admin.ModelAdmin):
    # Override the get_form method to conditionally hide the user field
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            form.base_fields.pop("store", None)

        return form

    def add_view(self, request, form_url="", extra_context=None):
        if not request.user.is_superuser:
            # Get the store of the logged-in user
            store = Store.objects.filter(user=request.user).first()
            if not store:
                messages.error(
                    request, "You don't have any store. Please create your store first."
                )
                return HttpResponse(
                    "You don't have any store. Please create your store first."
                )  # You can customize this message
            elif store and store.status != "Active":

                # Store is not active, show an error message and do not render the form
                messages.error(
                    request,
                    "Your store is not active. Please wait until your store is activated before adding products.",
                )
                return HttpResponse(
                    "Your store is not active. Please wait until your store is activated before adding products."
                )  # You can customize this message

        # If store is active, proceed with the usual add view
        return super().add_view(request, form_url, extra_context)

    # Automatically assign the logged-in user as the user for the Store
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            store = Store.objects.filter(user=request.user).first()
            obj.store = store
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Limit queryset to products that belong to the logged-in user's store."""
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            # Only show products linked to the store owned by the logged-in user
            queryset = queryset.filter(store__user=request.user)
        return queryset
    
    # Method to display the image in the list view
    def display_image(self, obj):
        if obj.image:
            # Return the HTML <img> tag to display the image in the admin table
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        else:
            return 'No image'  # Optional: Return text if no image is available
    display_image.short_description = 'Product Image'  # Column name in the admin table


    list_display = ("name", "price", "status", "display_image")  # Show store information
    search_fields = ("name", "price", "status")



# Register models in admin
admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
