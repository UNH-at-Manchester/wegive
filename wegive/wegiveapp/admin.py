from django.contrib import admin
from .models import Charity, Donor


# Register your models here.

admin.site.register(Charity)
admin.site.register(Donor)
