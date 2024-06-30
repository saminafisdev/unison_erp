from django.conf import settings
from django.db import models


class UnitOfMeasurement(models.Model):
    """Represents a unit of measurement (e.g. piece, box, kg, etc.)"""

    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    """Represents a category of products (e.g. electronics, furniture, etc.)"""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    """Represents a product in the inventory"""

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    """Represents the current inventory of a product"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.product.unit_of_measurement.abbreviation}"


class StockReceipt(models.Model):
    """Represents a receipt of new stock into the inventory"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Stock receipt for {self.product.name} on {self.date_received}"


class StockIssue(models.Model):
    """Represents an issue of stock from the inventory"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_issued = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField()
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    issued_to = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Stock issue for {self.product.name} on {self.date_issued}"


class StockAdjustment(models.Model):
    """Represents an adjustment to the inventory (e.g. stocktake, damage, etc.)"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_adjusted = models.DecimalField(max_digits=10, decimal_places=2)
    adjustment_reason = models.CharField(max_length=255)
    date_adjusted = models.DateField()
    adjusted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Stock adjustment for {self.product.name} on {self.date_adjusted}"
