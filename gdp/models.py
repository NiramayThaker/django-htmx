from django.db import models


# Create your models here.
class GDP(models.Model):
	country_code = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	year = models.PositiveSmallIntegerField()
	gdp = models.FloatField()

	def __str__(self):
		return f"{self.country}"
