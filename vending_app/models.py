from django.db import models
from django.utils.timezone import now

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name

class Machine(models.Model):
    location = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=20, unique=True)  # Fixed duplicate unique=True

    def __str__(self):
        return f"Machine {self.unique_id} at {self.location}"

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    change = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Added default=0.00
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"
