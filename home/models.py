from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class categories(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=50)
  image = models.ImageField(upload_to='products/', null=True, blank=True)

  def __str__(self):
    return self.name

class products(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=50)
  price = models.IntegerField()
  image = models.ImageField(upload_to='products/', null=True, blank=True)
  category = models.ForeignKey('categories', on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.name
    

class order(models.Model):
  STATUS_CHOICE = [
    ('pending', 'pending'),
    ('completed', 'completed'),
  ]

  name = models.CharField(max_length=50)
  phone_number = models.CharField(
        max_length=15,  
        validators=[
            RegexValidator(
                regex=r'^((\+92)?(0092)?(92)?(0)?3[0-9]{9})$',  
                message="Enter a Pakistan phone number in format +92xxxxxxxxxx"
            )
        ]
    )
  email = models.EmailField(max_length=254)
  address = models.TextField()
  product = models.ForeignKey("products", on_delete=models.CASCADE)
  prod_quantity = models.IntegerField()
  total_price = models.IntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='pending')

  def __str__(self):
    return f'Order #{self.id} by {self.name}'


class contactUs(models.Model):
  name = models.CharField(max_length=50)
  email = models.EmailField(max_length=254)
  phone_number = models.CharField(
        max_length=15,  
        validators=[
            RegexValidator(
                regex=r'^((\+92)?(0092)?(92)?(0)?3[0-9]{9})$',  
                message="Enter a Pakistan phone number in format +92xxxxxxxxxx"
            )
        ]
    )
  message = models.TextField()

  def __str__(self):
    return self.email