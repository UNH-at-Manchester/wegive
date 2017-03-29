from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Charity(models.Model):
    name = models.CharField(max_length=2000, null=False, blank=False)
    address = models.TextField(null=False, default="")
    location_x = models.FloatField(null=False, default=1000.0);
    location_y = models.FloatField(null=False, default=1000.0)
    phone = models.TextField(null=False, default="")
    cause = models.TextField(null=False, default="")
    tags_csv = models.TextField(null=False, default="", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False,
                                blank=False)

    def __str__(self):
        return "{} ({})".format(self.user, self.name)


class Donor(models.Model):
    name =  models.CharField(max_length=2000, null=False, blank=False)
    address = models.TextField(null=False)
    phone = models.TextField(null=False)
    date_of_birth = models.TextField(null=False)
    tags_csv = models.TextField(null=False, default="", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False,
                                blank=False)


    def __str__(self):
        return "{} ({})".format(self.user, self.name)

class Donation(models.Model):
    """
    Model for donation records. All currencies USD.

    Fields:
    Donor donor: The donor who made the donation.
    Charity charity: The charity the donation was made to.
    Decimal amount: The dollar amount. This is a Python decimal object, not a
                    float, so we don't have to worry about precision.
    DateTime time: The date and time at which the donation took place.
    """
    donor = models.OneToOneField(Donor, on_delete=models.CASCADE)
    charity = models.OneToOneField(Charity, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=3, null=False,
                                 blank=False)
    time = models.DateTimeField(auto_now_add=True, null=False, blank=False)
