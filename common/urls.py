from django.urls import path
from common.views import DashboardInsightsApiView

app_name = 'common'

urlpatterns = [
    path('dashboard/', DashboardInsightsApiView.as_view(), name='dashboard-insights'),
]

