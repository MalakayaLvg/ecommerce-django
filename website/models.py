from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    image = models.ImageField(upload_to='products/',null=True)

class Comment(models.Model):
    content = models.TextField()
    rate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

