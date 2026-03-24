from django.contrib import admin
from .models import sellerRegisteredTable, Vehicle, RTODatabase

# Register your models here.
admin.site.register(sellerRegisteredTable)
admin.site.register(Vehicle)
admin.site.register(RTODatabase)