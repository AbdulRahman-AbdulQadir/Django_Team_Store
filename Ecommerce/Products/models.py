from django.db import models
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='uploads/products/', blank=True, null=True)
    image_1 = models.ImageField(upload_to='uploads/products/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='uploads/products/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='uploads/products/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='uploads/products/', blank=True, null=True)
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    items = models.JSONField(
        help_text='[{"product_id": ..., "quantity": ..., "price": ...}, ...]',
        default=list,
        blank=True
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        total = 0
        for item in self.items or []:
            total += item.get('quantity', 0) * item.get('price', 0)
        self.total_price = total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.status} (Total: {self.total_price})"

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    items = models.JSONField(
        help_text='[{"product_id": ..., "quantity": ...}, ...]',
        default=list,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.customer.user.username}"
