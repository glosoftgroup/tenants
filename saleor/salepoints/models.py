from __future__ import unicode_literals
from django.db import models


class SalePoint(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	description = models.CharField(max_length=300, null=True, blank=True)

	def __str__(self):
		return str(self.name)
