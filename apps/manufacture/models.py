from django.db import models
from apps.contact.models import Contacts
from apps.product.models import ProductTemplate
from apps.employee.models import Employee
from apps.stock.models import StockLocation,StockMove

class Manufacture(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in-process', 'In Process'),
        ('in-process', 'In Process'),
    )
    mo_number = models.BigAutoField(primary_key=True)
    date = models.DateTimeField()
    customer = models.ForeignKey(Contacts,on_delete=models.CASCADE,related_name="contact")
    product = models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,related_name="manufacture_product")
    produced_qty = models.IntegerField()
    duration = models.DecimalField(max_digits=100, decimal_places=2)
    operator = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="employee")
    status = models.CharField(choices=STATUS,max_length=20,default='draft')
    location = models.ForeignKey(StockLocation,on_delete=models.CASCADE,related_name="location_of_stock")

    def total_raw_material_cost(self):
        pass
    
    def total_manufacturing_cost(self):
        pass

    def set_done(self):
        # Create stock moves for finished goods
        StockMove.objects.create(
            product=self.product,
            quantity=self.produced_qty,
            location_to=self.location,
            reference=f"MO-{self.mo_number}",
            move_type='manufacture',
            done=True
        )
        # Create stock moves for raw materials
        for raw in self.raw_materials.all():
            StockMove.objects.create(
                product=raw.raw_material,
                quantity=raw.quantity_used,
                location_from=self.location,
                reference=f"MO-{self.mo_number}",
                move_type='manufacture',
                done=True
            )
        
        self.status = 'done'
        self.save()

    def __str__(self):
        return self.moNumber


class ManufacturingOrderRawMaterial(models.Model):
    mo = models.ForeignKey(Manufacture,on_delete=models.CASCADE)
    raw_material = models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,limit_choices_to={'category__name': 'Raw Materials'},related_name="raw_materials")
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2)

    def total_cost (self):

        return 'x'
        
    def __str__(self):

        return f"{self.mo.mo_number} - {self.quantity_used}"


    


    

