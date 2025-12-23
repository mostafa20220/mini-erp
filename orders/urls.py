from django.urls import path
from orders.views import (
    ListCreateOrdersApiView,
    RetrieveUpdateDestroyOrderApiView,
    OrderItemsListApiView
)

app_name = 'orders'

urlpatterns = [
    path('', ListCreateOrdersApiView.as_view(), name='list-create-orders'),
    path('<int:pk>/', RetrieveUpdateDestroyOrderApiView.as_view(), name='retrieve-update-destroy-order'),
    path('<int:order_id>/items/', OrderItemsListApiView.as_view(), name='order-items'),
]

