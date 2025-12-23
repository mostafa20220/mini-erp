from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel
from users.constants import USER_ROLE_CHOICES, ROLE_ADMIN
from users.querysets import UserManager


class User(AbstractUser, BaseModel):

    # Identifiers
    email = models.EmailField(unique=True)
    customer_code = models.CharField(unique=True, max_length=100 ,blank=True, null=True)
    phone = PhoneNumberField(_("Phone Number"), unique=True,  blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default=ROLE_ADMIN, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    # info fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    # files
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True)

    # others
    username = models.CharField(max_length=50, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}> ({self.role}) [ID: {self.pk}]"