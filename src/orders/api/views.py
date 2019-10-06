from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (ListCreateAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateDestroyAPIView)

from one_order.config.greek_search_filter import GreekSearchFilter
from one_order.config.mixins import RequestLogViewMixin
from one_order.config.rest.paginations import StandardResultsSetPagination
from orders.models import Customer, Order, OrderType, Supplier
from .serializers import (CustomerSerializer, OrderPostSerializer,
                          OrderRetrieveSerializer, OrderTypeSerializer,
                          SupplierSerializer)


class CustomerListCreateAPIView(RequestLogViewMixin, ListCreateAPIView):
    """
    This endpoint is used to list and create customers\n
    GET method -> List\n
    POST method -> Create
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [OrderingFilter, GreekSearchFilter]
    ordering = ['first_name', 'last_name', 'email', 'publish_date', 'update_date']
    search_fields = ['first_name_latin', 'last_name_latin', 'email', 'home_phone', 'mobile_phone', 'comments_latin']
    pagination_class = StandardResultsSetPagination


class CustomerRUDAPIView(RequestLogViewMixin, RetrieveUpdateDestroyAPIView):
    """
    This endpoint is used to retrieve, update and delete a customer based on his id\n
    GET method -> Retrieve\n
    PUT method -> Update\n
    PATCH method -> Partial Update\n
    DELETE method -> Delete
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SupplierListCreateAPIView(RequestLogViewMixin, ListCreateAPIView):
    """
    This endpoint is used to list and create suppliers\n
    GET method -> List\n
    POST method -> Create
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [OrderingFilter, GreekSearchFilter]
    ordering = ['publish_date']
    ordering_fields = ['name', 'phone_number', 'email', 'publish_date', 'update_date']
    search_fields = ['name_latin', 'phone_number', 'email', 'comments_latin']
    pagination_class = StandardResultsSetPagination


class SupplierRUDAPIView(RequestLogViewMixin, RetrieveUpdateDestroyAPIView):
    """
    This endpoint is used to retrieve, update and delete a supplier based on his id\n
    GET method -> Retrieve\n
    PUT method -> Update\n
    PATCH method -> Partial Update\n
    DELETE method -> Delete
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class OrderTypeListCreateAPIView(RequestLogViewMixin, ListCreateAPIView):
    """
    This endpoint is used to list and create available order types\n
    GET method -> List\n
    POST method -> Create
    """
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer
    filter_backends = [OrderingFilter, GreekSearchFilter]
    ordering = ['publish_date']
    ordering_fields = ['title', 'publish_date', 'update_date']
    search_fields = ['title_latin', 'comments_latin']
    pagination_class = StandardResultsSetPagination


class OrderTypeRUDAPIView(RequestLogViewMixin, RetrieveUpdateDestroyAPIView):
    """
    This endpoint is used to retrieve, update and delete an order type based on its id\n
    GET method -> Retrieve\n
    PUT method -> Update\n
    PATCH method -> Partial Update\n
    DELETE method -> Delete
    """
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer


class OrderListCreateAPIView(RequestLogViewMixin, ListCreateAPIView):
    """
    This endpoint is used to list and create orders\n
    GET method -> List\n
    POST method -> Create
    """
    queryset = Order.objects.filter(is_deleted=False)
    filter_backends = [DjangoFilterBackend, OrderingFilter, GreekSearchFilter]
    ordering = ['publish_date']
    ordering_fields = ['customer__last_name', 'customer__email', 'supplier__name', 'type__title', 'product',
                       'expiration_date', 'publish_date', 'update_date']
    search_fields = ['customer__first_name_latin', 'customer__last_name_latin', 'customer__email', 'customer__home_phone',
                     'customer__mobile_phone',
                     'user__username', 'product_latin', 'supplier__name_latin', 'comments_latin']
    filter_fields = ['type__title', 'status', 'is_deleted']
    pagination_class = StandardResultsSetPagination

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderPostSerializer
        return OrderRetrieveSerializer


class OrderRUDAPIView(RequestLogViewMixin, RetrieveDestroyAPIView):
    """
    This endpoint is used to retrieve, update and delete an order based on its id\n
    GET method -> Retrieve\n
    PUT method -> Update\n
    PATCH method -> Partial Update\n
    DELETE method -> Delete
    """
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderRetrieveSerializer
        return OrderPostSerializer
