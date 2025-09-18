from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_products', kwargs={'slug': self.slug})

class Product(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sub_category = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='GH₵')
    short_description = models.TextField(max_length=500)
    long_description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    # Optional: filename for a static image committed to the repo under static/products/
    # Example: "laptop-123.jpg" (do not include leading slashes)
    image_static = models.CharField(max_length=255, blank=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Product attributes as JSON field (for flexible attributes)
    processor = models.CharField(max_length=100, blank=True)
    ram = models.CharField(max_length=50, blank=True)
    storage = models.CharField(max_length=100, blank=True)
    screen_size = models.CharField(max_length=50, blank=True)
    other_attributes = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"{self.category.name[:3].upper()}{str(uuid.uuid4())[:8]}"
        super().save(*args, **kwargs)

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('IT', 'IT Services'),
        ('DIGITAL', 'Digital Services'),
        ('EDUCATION', 'Educational Services'),
        ('BUSINESS', 'Business Services'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    duration_estimate = models.CharField(max_length=100, blank=True)
    price_range = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=10, default='')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default='Wa')
    region = models.CharField(max_length=100, default='Upper West')
    country = models.CharField(max_length=100, default='Ghana')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('PROCESSING', 'Processing'),
        ('READY', 'Ready for Pickup'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('MOMO', 'Mobile Money'),
        ('CASH', 'Cash on Delivery'),
        ('BANK', 'Bank Transfer'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='MOMO')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    order_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='NEW')
    customer_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"NG{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def get_total_price(self):
        return self.quantity * self.price_at_purchase

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
