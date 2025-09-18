from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from django.templatetags.static import static
from .models import Category, Product, Service, Customer, Order, OrderItem, ContactMessage

# Custom Admin Site Configuration
admin.site.site_header = "Nicky G. Computers Admin"
admin.site.site_title = "Nicky G. Admin"
admin.site.index_title = "Welcome to Nicky G. Computers Administration"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'product_count']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price_display', 'stock_status', 'is_featured', 'is_active']
    list_filter = ['category', 'brand', 'is_featured', 'is_active']
    search_fields = ['name', 'brand', 'sku', 'short_description']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'category', 'brand', 'sku')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'long_description')
        }),
        ('Image', {
            'fields': ('image', 'image_static', 'image_preview')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
    )
    
    def price_display(self, obj):
        return f"GH₵ {obj.price:,.2f}"
    price_display.short_description = 'Price'
    
    def stock_status(self, obj):
        if obj.stock > 10:
            color = 'green'
            status = f'In Stock ({obj.stock})'
        elif obj.stock > 0:
            color = 'orange'
            status = f'Low Stock ({obj.stock})'
        else:
            color = 'red'
            status = 'Out of Stock'
        return format_html(f'<span style="color: {color}; font-weight: bold;">{status}</span>')
    stock_status.short_description = 'Stock Status'
    
    def image_preview(self, obj):
        # Prefer static image if provided
        if getattr(obj, 'image_static', None):
            url = static(f"products/{obj.image_static}")
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', url)
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_display', 'is_featured', 'is_active']
    list_filter = ['is_featured', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_featured', 'is_active']
    
    def price_display(self, obj):
        return f"GH₵ {obj.price:,.2f}"
    price_display.short_description = 'Price'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'order_count', 'total_spent', 'created_at']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at']
    
    def order_count(self, obj):
        return obj.orders.count()
    order_count.short_description = 'Orders'
    
    def total_spent(self, obj):
        total = sum(order.total_amount for order in obj.orders.all())
        return f"GH₵ {total:,.2f}"
    total_spent.short_description = 'Total Spent'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price_at_purchase', 'total_price']
    
    def total_price(self, obj):
        return f"GH₵ {obj.quantity * obj.price_at_purchase:,.2f}"
    total_price.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_info', 'total_display', 'status_display', 'created_at']
    list_filter = ['order_status', 'created_at']
    search_fields = ['id', 'customer__name', 'customer__phone']
    readonly_fields = ['created_at', 'order_summary']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'customer', 'order_status', 'created_at')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'total_amount')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
        ('Summary', {
            'fields': ('order_summary',)
        }),
    )
    
    def order_number(self, obj):
        return f"ORD-{obj.id:06d}"
    order_number.short_description = 'Order #'
    
    def customer_info(self, obj):
        return format_html(
            '<strong>{}</strong><br/>Phone: {}<br/>Email: {}',
            obj.customer.name,
            obj.customer.phone,
            obj.customer.email or 'No email'
        )
    customer_info.short_description = 'Customer'
    
    def total_display(self, obj):
        return f"GH₵ {obj.total_amount:,.2f}"
    total_display.short_description = 'Total'
    
    def status_display(self, obj):
        colors = {
            'NEW': 'orange',
            'PROCESSING': 'blue',
            'READY': 'purple',
            'COMPLETED': 'green',
            'CANCELLED': 'red'
        }
        color = colors.get(obj.order_status, 'gray')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.order_status.upper()
        )
    status_display.short_description = 'Status'
    
    def order_summary(self, obj):
        items = obj.items.all()
        summary = "<h3>Order Items:</h3><ul>"
        for item in items:
            summary += f"<li>{item.product.name} - Qty: {item.quantity} - GH₵ {item.price_at_purchase:,.2f} each</li>"
        summary += "</ul>"
        return mark_safe(summary)
    order_summary.short_description = 'Order Summary'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject_display', 'created_at', 'read_status', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_editable = ['is_read']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def subject_display(self, obj):
        return obj.subject
    subject_display.short_description = 'Subject'
    
    def read_status(self, obj):
        if obj.is_read:
            return format_html('<span style="color: green;">Read</span>')
        else:
            return format_html('<span style="color: red;">Unread</span>')
    read_status.short_description = 'Status'
