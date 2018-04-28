from django.contrib.auth.models import AbstractUser
from django.db import models

from django_countries.fields import CountryField

ADMIN       = '1'
MANAGER     = '2'
DISTRIBUTOR = '3'
CUSTOMER    = '4'

USER_TYPE_CHOICES = (
    (ADMIN, 'Admin'),
    (MANAGER, 'Manager'),
    (DISTRIBUTOR, 'Distributor'),
    (CUSTOMER, 'Customer'),
)

class User(AbstractUser):
    user_type           = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, default=CUSTOMER)
    adress              = models.CharField(max_length=220, null=True, blank=True)
    postcode            = models.PositiveSmallIntegerField(null=True, blank=True)
    country             = CountryField()

    def __str_(self):
        return self.username

class Distributor(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    brand               = models.CharField(max_length=100)
    ceo_name            = models.CharField(max_length=100)
    average_earnings    = models.PositiveIntegerField()
    company_created_At  = models.DateField(auto_now=False, auto_now_add=False)
    is_approveled       = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
