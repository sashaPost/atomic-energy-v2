from django.contrib import admin
from .models import Procurement, Unit

# Register your models here.

admin.site.register(Unit)
admin.site.register(Procurement)