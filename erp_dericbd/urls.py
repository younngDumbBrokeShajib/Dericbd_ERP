
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("apps.core.urls")),
    path('',include("apps.product.urls")),
    path('',include("apps.contact.urls")),
    path('',include("apps.manufacture.urls")),
    path('',include("apps.employee.urls")),
    path('',include("apps.stock.urls")),
]
