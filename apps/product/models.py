from django.db import models

# Create your models here.
class ProductCategory (models.Model):
    name = models.CharField('Product category',max_length=100)

class Packaging(models.Model):
    PACKAGE_TYPES = (
        ('bag', 'Bag'),
        ('drum', 'Drum'),
    )

    name = models.CharField('Package Name',max_length=100)
    net_unit = models.IntegerField('Units in the package')
    weight = models.FloatField('Total package weight')
    package_type = models.CharField('Package type',choices=PACKAGE_TYPES,max_length=10,default='bag')



class ProductTemplate(models.Model):
    name = models.CharField('Product Name',max_length=255)
    code = models.CharField('Product Code',max_length=10)
    sales_price = models.FloatField('Product sales price')
    cost_per_unit = models.FloatField('Product cost per unit')
    sale_ok = models.BooleanField('Sale ok?',default=True)
    purchase_ok = models.BooleanField('Purchase Ok?',default=True)
    package = models.ForeignKey(Packaging,on_delete=models.CASCADE,related_name="package")
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,related_name="category")

    # product_bom = mdoels.ForeignKey(model_name,on_delete=models.SET_NULL,related_name="bom")

class ProductVariant(models.Model):
    product = models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,related_name="product")
    sku = models.CharField(max_length=300)
    lot_code = models.CharField(max_length=300)
    weight = models.FloatField()

class BillOfMaterials(models.Model):
    product=models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,related_name="product_bom")
    raw_material=models.ForeignKey(ProductTemplate,on_delete=models.CASCADE,limit_choices_to={'category__name': 'Raw Materials'})
    quantity_per_unit=models.FloatField()
    finished_product_qunatity=models.FloatField()
    
