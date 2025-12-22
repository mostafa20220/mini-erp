from django.urls import path
from products.views import (
    ListCreateProductsApiView,
    RetrieveUpdateDestroyProductApiView,
    ProductStockHistoryApiView
)

urlpatterns = [
    path('', ListCreateProductsApiView.as_view(), name='list-create-products'),
    path('<int:pk>/', RetrieveUpdateDestroyProductApiView.as_view(), name='retrieve-update-destroy-product'),
    path('stock-history/', ProductStockHistoryApiView.as_view(), name='product-stock-history'),
]