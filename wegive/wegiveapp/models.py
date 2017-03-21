from django.db import models

# Create your models here.
class Charity(models.Model):
    name = models.CharField(max_length=2000, null=False, blank=False)
    address = models.TextField(null=False, default="")
    location_x = models.FloatField(null=False, default=1000.0);
    location_y = models.FloatField(null=False, default=1000.0)
    phone = models.TextField(null=False, default="")
    cause = models.TextField(null=False, default="")

    def __str__(self):
        return self.name


class Donor(models.Model):
    name =  models.CharField(max_length=2000, null=False, blank=False)
    address = models.TextField(null=False)
    phone = models.TextField(null=False)
    date_of_birth = models.TextField(null=False)


    def __str__(self):
        return self.name
