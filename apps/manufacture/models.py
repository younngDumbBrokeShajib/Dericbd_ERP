from django.db import models
from apps.contact.models import Contacts
from apps.product.models import ProductTemplate
from apps.employee.models import Employee
from apps.stock.models import StockLocation,StockMove
# Create your models here.

class Manufacture(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in-process', 'In Process'),
        ('confirmed', 'Confirmed'),
        ('done','Done'),
    )
    mo_number = models.BigAutoField(primary_key=True)
    date = models.DateTimeField()
    customer = models.ForeignKey(Contacts,on_delete=models.CASCADE,related_name="contact")
    product = models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,related_name="manufacture_product")
    produced_qty = models.IntegerField()
    duration = models.DecimalField(max_digits=100, decimal_places=2)
    operator = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="employee")
    status = models.CharField(choices=STATUS,max_length=20,default='draft')
    #location_to = models.ForeignKey(StockLocation,on_delete=models.CASCADE,related_name="location_of_stock")
    location_from = models.ForeignKey(StockLocation, on_delete=models.CASCADE, related_name="mo_raw_material_location",null=True,blank=True)
    location_to = models.ForeignKey(StockLocation, on_delete=models.CASCADE, related_name="mo_finished_product_location",null=True,blank=True)

    def total_raw_material_cost(self):

        raw_cost_sum=sum(items.total_cost() for items in self.raw_materials.all())
        return raw_cost_sum


    def total_manufacturing_cost(self):
        pass

    def set_done(self):

        """Confirm MO, consume raw materials, and produce finished goods."""
        if self.status != "draft":
            raise ValueError("Manufacturing Order must be in draft state to confirm.")

        # Create stock moves for finished goods
        StockMove.objects.create(
            product=self.product,
            quantity=self.produced_qty,
            location_to=self.location_to,
            reference=f"MO-{self.mo_number}",
            move_type='manufacture',
            done=False
        )
        # Create stock moves for raw materials
        for mo_raw_material in self.mo_raw_materials.all():
            StockMove.objects.create(
                product=mo_raw_material.raw_material,
                quantity=mo_raw_material.quantity_used * self.produced_qty,
                location_from=self.location_from,
                reference=f"MO-{self.mo_number}",
                move_type='manufacture',
                done=False
            )
        
        self.status = 'confirmed' 
        #after the stock_move method is done , mo will confirm -> Done state
        self.save()

    def complete_manufacturing(self):
        """Finalize MO and update stock."""
        if self.status != "confirmed":
            raise ValueError("Manufacturing Order must be confirmed before completion.")

        # Process all stock moves
        for move in StockMove.objects.filter(reference__startswith=f"MO-{self.id}"):
            move.process_move()

        self.status = "done" #done state as te stock.move method has been processed
        self.save()
    
    
    def __str__(self):
        return self.mo_number


class ManufacturingOrderRawMaterial(models.Model):
    mo = models.ForeignKey(Manufacture,on_delete=models.CASCADE,related_name='mo_raw_materials')
    raw_material = models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,limit_choices_to={'category__name': 'Raw Materials'},related_name="raw_materials")
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2)

    def total_cost (self):

         return self.quantity_used*self.raw_material.cost_per_unit
        
    def __str__(self):

        return f"{self.mo.mo_number} - {self.quantity_used}"


    


    

