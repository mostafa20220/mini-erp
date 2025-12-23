from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from users.models import User
from orders.models import Order
from products.models import Product
from users.permissions import IsSales, IsAdmin


class DashboardInsightsApiView(APIView):

    permission_classes = [IsAdmin | IsSales]

    def get(self, request):

        total_customers = User.objects.customers().count()
        today_sales = Order.objects.today_sales()
        low_stock_products = (Product.objects.low_stock()
                              .values('id', 'sku', 'name', 'stock_qty'))
        out_of_stock_count = Product.objects.out_of_stock().count()
        today = timezone.now().date().isoformat()

        return Response({
            'total_customers': total_customers,
            'total_sales_today': float(today_sales),
            'low_stock_products': list(low_stock_products),
            'low_stock_count': low_stock_products.count(),
            'out_of_stock_count': out_of_stock_count,
            'date': today
        })

