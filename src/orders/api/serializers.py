from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from one_order.config.constants import PRESCRIPTIONS_EXPIRING
from orders.models import Customer, Order, OrderType, Supplier


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('first_name_latin', 'last_name_latin', 'comments_latin')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class OrderTypeSerializer(ModelSerializer):
    class Meta:
        model = OrderType
        exclude = ('title_latin', 'comments_latin')


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ('name_latin', 'comments_latin')


class OrderPostSerializer(ModelSerializer):
    class Meta:
        model = Order
        exclude = ('product_latin', 'comments_latin')


class OrderRetrieveSerializer(ModelSerializer):
    type = OrderTypeSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)
    expiring = SerializerMethodField()
    expired = SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_expiring(self, obj):
        if (obj.status == "Delivered" or obj.expired()):
            return False
        now = timezone.now()
        try:
            if (obj.expiration_date <= now + timedelta(days=PRESCRIPTIONS_EXPIRING)):
                return True
            else:
                return False
        except:
            return False

    def get_expired(self, obj):
        if obj.status == "Delivered":
            return False
        now = timezone.now()
        try:
            if (obj.expiration_date < now):
                return True
            else:
                return False
        except:
            return False
