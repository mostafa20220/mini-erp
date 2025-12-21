from django.urls import path
from .views import ListCreateProductsApiView

urlpatterns = [
    path('', ListCreateProductsApiView.as_view(), name='list-create-products'),
    path('<int:pk>/', ListCreateProductsApiView.as_view(), name='retrieve-update-destroy-product'),
]