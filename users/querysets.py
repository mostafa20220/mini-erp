from django.contrib.auth.models import BaseUserManager
from django.db import models
from users.constants import ROLE_CUSTOMER, ROLE_ADMIN, ROLE_SALES_USER


class UserQuerySet(models.QuerySet):

    def customers(self):
        return self.filter(role=ROLE_CUSTOMER)

    def sales_users(self):
        return self.filter(role=ROLE_SALES_USER)

    def admins(self):
        return self.filter(role=ROLE_ADMIN)

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def list_customers_query(self):
        return (self
                .filter(
                    role=ROLE_CUSTOMER,
                    is_active=True,
                )
                .select_related(
                    'created_by',
                    'modified_by',
                )
                .only(
                    'id',
                    'customer_code',
                    'email',
                    'phone',
                    'first_name',
                    'last_name',
                    'address',
                    'opening_balance',
                    'created_at',
                    'modified_at',
                    'created_by__id',
                    'created_by__first_name',
                    'created_by__last_name',
                    'modified_by__id',
                    'modified_by__first_name',
                    'modified_by__last_name',
                )
                .order_by('-id'))


class UserManager(BaseUserManager):

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def customers(self):
        return self.get_queryset().customers()

    def sales_users(self):
        return self.get_queryset().sales_users()

    def admins(self):
        return self.get_queryset().admins()

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

    def list_customers_query(self):
        return self.get_queryset().list_customers_query()

