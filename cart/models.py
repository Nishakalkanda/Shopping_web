from django.db import models
from django.contrib.auth.models import User
from Products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def subtotal(self):
        return self.quantity * self.product.price
    


class Address(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=50)

    state = models.CharField(max_length=50)

    pincode = models.CharField(max_length=10)          
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Paid','Paid'),
        ('Packed','Packed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES, default='Pending')
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at =  models.DateTimeField(auto_now_add=True)
    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
        
        