from django.db import models
from apps.product.models import ProductTemplate,ProductVariant

# Create your models here.
class StockLocation(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    active = models.BooleanField()

class StockQuant(models.Model):
    product = models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,related_name="stock_product")
    variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name="stock_product_variant")
    location = models.ForeignKey(StockLocation,on_delete=models.CASCADE,related_name="stock_location")
    quantity = models.IntegerField()
    reserved_quantity = models.IntegerField()

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity
    
class StockMove(models.Model):
    MOVE_TYPE = {
        "manufacturing": "Manufacturing",
        "in": "In",
        "out": "Out",
        "adjustment": "Adjustment",
    }
    product  = product = models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,related_name="stock_move_product")
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    location_from = models.ForeignKey(StockLocation,on_delete=models.CASCADE,related_name="stock_location_from") 
    location_to  = models.ForeignKey(StockLocation,on_delete=models.CASCADE,related_name="stock_location_to") 
    reference  = models.CharField(max_length=500)
    move_type = models.CharField(choices=MOVE_TYPE,max_length=50)
    date = models.DateField()
    done = models.BooleanField()

    def save(self, *args, **kwargs):
        pass

    def process_move(self):
        pass


