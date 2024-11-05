from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])