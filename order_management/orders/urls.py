from django.urls import path
from . import views
from .views import OrdersListView,OrdersDetailView,OrdersCreateView,OrdersUpdateView,OrdersDeleteView

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders-home'),
    path('orders/<int:pk>/', OrdersDetailView.as_view(), name='orders-detail'),
    path('orders/<int:pk>/update/', OrdersUpdateView.as_view(), name='orders-update'),
    path('orders/<int:pk>/delete/', OrdersDeleteView.as_view(), name='orders-delete'),
    path('order/new/', OrdersCreateView.as_view(), name='order-create'),
    path('about/', views.about, name='orders-about'),
]