from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsSales, IsAdmin
from users.querysets import UserQuerySet
from users.serializers import LogoutSerializer, CreateCustomerSerializer, ReadCustomerSerializer, \
    UpdateCustomerSerializer


class LogoutView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer


class ListCreateCustomerApiView(ListCreateAPIView):
    queryset = UserQuerySet.list_customers_query()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCustomerSerializer
        return ReadCustomerSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsSales | IsAdmin]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

class RetrieveUpdateDestroyCustomerApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = UserQuerySet.list_customers_query()

    def get_serializer_class(self):
        method_map = {
            'GET': ReadCustomerSerializer,
            'PUT': UpdateCustomerSerializer,
            'PATCH': UpdateCustomerSerializer,
        }
        return method_map.get(self.request.method, ReadCustomerSerializer)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)
