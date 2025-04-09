from django.contrib import admin
from .models import ProductTemplate,ProductCategory,Packaging,ProductVariant,BillOfMaterials
# Register your models here.

admin.site.register(ProductVariant)
admin.site.register(ProductCategory)
admin.site.register(ProductTemplate)
admin.site.register(BillOfMaterials)
