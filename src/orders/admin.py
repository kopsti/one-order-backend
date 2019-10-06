from django.contrib import admin

from one_order.config.utils import admin_link
from .models import Customer, Order, OrderType, Supplier


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'home_phone', 'mobile_phone', 'email']
    readonly_fields = ['first_name_latin', 'last_name_latin', 'publish_date', 'update_date', 'comments_latin']
    search_fields = ['first_name', 'last_name', 'home_phone', 'mobile_phone', 'email']
    save_on_top = True


@admin.register(OrderType)
class OrderTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    readonly_fields = ['title_latin', 'comments_latin', 'publish_date', 'update_date']
    search_fields = ['title', 'comments']
    save_on_top = True


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_number']
    readonly_fields = ['name_latin', 'comments_latin', 'publish_date', 'update_date']
    search_fields = ['name', 'phone_number']
    save_on_top = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_link', 'user_link', 'supplier_link', 'type_link', 'status', 'expiration_date',
                    'expiring', 'expired']
    readonly_fields = ['expiring', 'expired', 'is_deleted', 'delete_date', 'publish_date', 'update_date']
    search_fields = ['custoemer__first_name', 'customer__last_name', 'customer__home_phone', 'customer__mobile_phone',
                     'customer__email', 'supplier__name']
    save_on_top = True

    @admin_link('customer', 'Customer')
    def customer_link(self, customer):
        return customer

    @admin_link('user', 'User')
    def user_link(self, user):
        return user

    @admin_link('supplier', 'Supplier')
    def supplier_link(self, supplier):
        return supplier

    @admin_link('type', 'OrderType')
    def type_link(self, type):
        return type
