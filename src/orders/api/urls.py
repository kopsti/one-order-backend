from django.urls import path

from .views import (CustomerListCreateAPIView, CustomerRUDAPIView,
                    OrderListCreateAPIView, OrderRUDAPIView,
                    OrderTypeListCreateAPIView, OrderTypeRUDAPIView,
                    SupplierListCreateAPIView, SupplierRUDAPIView)

urlpatterns = [
    path('suppliers/', SupplierListCreateAPIView.as_view()),
    path('suppliers/<int:pk>/', SupplierRUDAPIView.as_view()),
    path('customers/', CustomerListCreateAPIView.as_view()),
    path('customers/<int:pk>/', CustomerRUDAPIView.as_view()),
    path('types/', OrderTypeListCreateAPIView.as_view()),
    path('types/<int:pk>/', OrderTypeRUDAPIView.as_view()),
    path('orders/', OrderListCreateAPIView.as_view()),
    path('orders/<int:pk>/', OrderRUDAPIView.as_view())
]
