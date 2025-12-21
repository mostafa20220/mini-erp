from users.constants import ROLE_CUSTOMER
from users.models import User


class UserQuerySet:

    @classmethod
    def list_customers_query(cls):
        return (User.objects
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