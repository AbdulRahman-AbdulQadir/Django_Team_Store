from django.db import models
from django.contrib.auth.models import User
from Products.models import Product

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)

    # Don't pluralize address
    class Meta:
        verbose_name_plural = "Shipping Address"
    def __str__(self):
        return f'Shipping Address - {str( self.id )}'
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # items = models.JSONField(
    #     help_text='[{"product_id": ..., "quantity": ..., "price": ...}, ...]',
    #     default=list,
    #     blank=True
    # )
    # updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     total = 0
    #     for item in self.items or []:
    #         total += item.get('quantity', 0) * item.get('price', 0)
    #     self.total_price = total
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Order - {str(self.id)}"

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'