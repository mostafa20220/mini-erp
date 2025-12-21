from django.urls import path

from users.views import ListCreateCustomerApiView, RetrieveUpdateDestroyCustomerApiView

urlpatterns = [
    path("", ListCreateCustomerApiView.as_view(), name="list-create-customer"),
    path("<int:pk>/", RetrieveUpdateDestroyCustomerApiView.as_view(), name="retrieve-update-destroy-customer"),
]
