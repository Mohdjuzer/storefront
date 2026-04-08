from django.contrib import admin
from . import models
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Count

class InventoryFilter(admin.SimpleListFilter):
    title = 'stock'
    parameter_name = 'stock'
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        
@admin.action(description='clear stock')    
def clear_stock(self, request, queryset):
            updated_count = queryset.update(inventory=0)
            self.message_user(request, f'{updated_count} products were successfully updated')    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [clear_stock]
    list_display = ['title', 'unit_price', 'Stock_update', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def Stock_update(self, product):
        if product.inventory < 10:
            return 'Less'
        return 'proper'
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10  
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        return customer.orders_count
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count = Count('order')
        )

class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    extra = 0    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer_name']
    list_select_related = ['customer']
    ordering = ['id', 'placed_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__email']
    inlines = [OrderItemInline]
    @admin.display(ordering='customer__first_name')
    def customer_name(self, order):
        return f'{order.customer.first_name} {order.customer.last_name}'

   
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>',url, collection.product_count)
        
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )
