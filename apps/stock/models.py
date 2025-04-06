from django.db import models
from apps.product.models import ProductTemplate,ProductVariant

# Create your models here.
class StockLocation(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    active = models.BooleanField()


#StockQuant is used for actual stock
#every product's qunatity gets updates as the stock move model creates an entry
class StockQuant(models.Model):
    product = models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,related_name="stock_product")
    variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name="stock_product_variant")
    location = models.ForeignKey(StockLocation,on_delete=models.CASCADE,related_name="stock_location")
    quantity = models.IntegerField()
    reserved_quantity = models.IntegerField()

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity
    
#StockMove model only holds the entires of items movement and quantity
#this does not represent the actualy stock
#this updates the quntity in and out 
class StockMove(models.Model):
    MOVE_TYPE = {
        "manufacturing": "Manufacturing",
        "in": "In",
        "out": "Out",
        "adjustment": "Adjustment",
    }
    product  = product = models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,related_name="stock_move_product")
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    location_from = models.ForeignKey(StockLocation,on_delete=models.CASCADE,related_name="stock_location_from",null=True,blank=True) 
    location_to  = models.ForeignKey(StockLocation,on_delete=models.CASCADE,related_name="stock_location_to",null=True,blank=True) 
    reference  = models.CharField(max_length=500)
    move_type = models.CharField(choices=MOVE_TYPE,max_length=50)
    date = models.DateField()
    done = models.BooleanField()

    def save(self, *args, **kwargs):
        pass

    def process_move(self):
        #pass

        """Process stock movement and update inventory levels."""
        if self.done:
            return  # Prevent duplicate processing

        if self.move_type == "out":
            # Deduct raw materials from stock
            try:
                stock_quant = StockQuant.objects.get(product=self.product, location=self.location_from)
                if stock_quant.quantity >= self.quantity:
                    stock_quant.quantity -= self.quantity
                    stock_quant.save()
                else:
                    raise ValueError(f"Not enough stock for {self.product.name}!")
            except StockQuant.DoesNotExist:
                raise ValueError(f"No stock found for {self.product.name} in {self.location_from.name}!")

        elif self.move_type == "in":
            # Add finished product to stock
            stock_quant, _ = StockQuant.objects.get_or_create(
                product=self.product, location=self.location_to,
                defaults={"quantity": 0, "reserved_quantity": 0}
            )
            stock_quant.quantity += self.quantity
            stock_quant.save()
        self.done = True
        self.save()