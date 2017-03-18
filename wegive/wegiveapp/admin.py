from django.contrib import admin
from .models import Charity, Donor


admin.site.register(Charity)# Register your models here.
admin.site.register(Donor)