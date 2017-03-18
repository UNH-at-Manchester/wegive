from django.db import models

# Create your models here.
class Charity(models.Model):
	name = models.CharField(max_length=2000,null=False)
	Address = models.TextField(null=False)
	Phone = models.TextField(null=False)
	cause = models.TextField(null=False)

	def __str__(self):
		return self.name


class Donor(models.Model):
	name = 	models.CharField(max_length=2000,null=False)
	Address = models.TextField(null=False)
	Phone = models.TextField(null=False)
	DOB = models.TextField(null=False)


	def __str__(self):
		return self.name