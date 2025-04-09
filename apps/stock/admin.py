from django.contrib import admin
from .models import StockLocation,StockMove,StockQuant
# Register your models here.

admin.site.register(StockLocation)
admin.site.register(StockMove)
admin.site.register(StockQuant)
