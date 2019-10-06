from datetime import date, timedelta

import unidecode
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from one_order.config.constants import (CHARFIELD_MAX, PRESCRIPTIONS_EXPIRING,
                                        TEXTFIELD_MAX)

phone_regex = RegexValidator(regex=r'^\d{1,20}$', message="Enter a valid phone number.")


class Customer(models.Model):
    first_name = models.CharField(max_length=CHARFIELD_MAX, help_text='The customer\'s first name.')
    first_name_latin = models.CharField(max_length=CHARFIELD_MAX,
                                        help_text='Helping property, used for efficient searching.')
    last_name = models.CharField(max_length=CHARFIELD_MAX, help_text='The customer\'s last name.')
    last_name_latin = models.CharField(max_length=CHARFIELD_MAX,
                                       help_text='Helping property, used for efficient searching.')
    home_phone = models.CharField(validators=[phone_regex], blank=True, null=True, max_length=CHARFIELD_MAX,
                                  help_text='The customer\'s home phone.')
    mobile_phone = models.CharField(validators=[phone_regex], blank=True, null=True, max_length=CHARFIELD_MAX,
                                    help_text='The customer\'s mobile phone.')
    email = models.EmailField(blank=True, null=True, help_text='The customer\'s email.')
    comments = models.TextField(blank=True, null=True, max_length=TEXTFIELD_MAX, help_text='The customer\'s comments.')
    comments_latin = models.TextField(blank=True, null=True, max_length=TEXTFIELD_MAX,
                                      help_text='Helping property, used for efficient searching.')
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=True, help_text='The customer\'s publish date.')
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False,
                                       help_text='The supplier\'s latest update date.')

    def __str__(self):
        return self.last_name + " " + self.first_name

    def save(self, *args, **kwargs):
        self.first_name_latin = unidecode.unidecode(self.first_name)
        self.last_name_latin = unidecode.unidecode(self.last_name)
        self.comments_latin = unidecode.unidecode(self.comments)
        super(Customer, self).save(*args, **kwargs)


ORDER_STATUS = (
    ("Pending", "Pending"),
    ("Ordered", "Ordered"),
    ("Received", "Received"),
    ("Delivered", "Delivered")
)


class OrderType(models.Model):
    title = models.CharField(max_length=CHARFIELD_MAX, help_text='The order type\'s title.', )
    title_latin = models.CharField(max_length=CHARFIELD_MAX, help_text='Helping property, used for efficient searching.')
    comments = models.TextField(blank=True, null=True, max_length=TEXTFIELD_MAX,
                                help_text='The order type\'s comments.')
    comments_latin = models.TextField(blank=True, null=True, max_length=TEXTFIELD_MAX,
                                      help_text='Helping property, used for efficient searching.')
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=True, help_text='The order type\'s publish date.')
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False,
                                       help_text='The order type\'s latest update date.')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title_latin = unidecode.unidecode(self.title)
        self.comments_latin = unidecode.unidecode(self.comments)
        super(OrderType, self).save(*args, **kwargs)


class Supplier(models.Model):
    name = models.CharField(max_length=CHARFIELD_MAX, help_text='The supplier\'s name.')
    name_latin = models.CharField(max_length=CHARFIELD_MAX, help_text='Helping property, used for efficient searching.')
    email = models.EmailField(blank=True, null=True, help_text='The suppliers\'s email.')
    comments = models.TextField(blank=True, null=True, max_length=TEXTFIELD_MAX, help_text='The supplier\'s comments.')
    comments_latin = models.TextField(blank=True, null=True, max_length=TEXTFIELD_MAX,
                                      help_text='Helping property, used for efficient searching.')
    phone_number = models.CharField(validators=[phone_regex], blank=True, null=True, max_length=CHARFIELD_MAX,
                                    help_text='The suppliers\'s phone number.')
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=True, help_text='The supplier\'s publish date.')
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False,
                                       help_text='The supplier\'s latest update date.')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name_latin = unidecode.unidecode(self.name)
        self.comments_latin = unidecode.unidecode(self.comments)
        super(Supplier, self).save(*args, **kwargs)


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL,
                                 help_text='The order\'s customer. Foreign key.')
    user = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'is_active': True},
                             help_text='The order\'s owner & author. Foreign key.')
    product = models.CharField(max_length=CHARFIELD_MAX, help_text='The product the order is about.')
    product_latin = models.CharField(max_length=CHARFIELD_MAX, help_text='Helping property, used for efficient searching.')
    supplier = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.SET_NULL,
                                 help_text='The order\'s product supplier. Foreign key.')
    type = models.ForeignKey(OrderType, null=True, on_delete=models.SET_NULL,
                             help_text='The order\'s type. Foreign key.')
    status = models.CharField(max_length=CHARFIELD_MAX, choices=ORDER_STATUS, default=ORDER_STATUS[0][0],
                              help_text='The order\'s status. May be one of {Pending, Ordered, Received, Delivered}.')
    expiration_date = models.DateField(blank=True, null=True, help_text='The order\'s due date.')
    comments = models.TextField(blank=True, null=True, max_length=TEXTFIELD_MAX, help_text='The order\'s comments.')
    comments_latin = models.TextField(blank=True, null=True, max_length=TEXTFIELD_MAX, help_text='Helping property, used for efficient searching.')
    is_deleted = models.BooleanField("Deleted", default=False, help_text='Denotes whether the user deleted this order.')
    delete_date = models.DateTimeField(blank=True, null=True, help_text='The date the user deleted the order.')
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=True, help_text='The order\'s publish date.')
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, help_text='The order\'s latest update date.')

    def __str__(self):
        return "%s for %s, %s" % (self.product, self.customer, self.user.get_full_name())

    def save(self, *args, **kwargs):
        self.product_latin = unidecode.unidecode(self.product)
        self.comments_latin = unidecode.unidecode(self.comments)
        super(Order, self).save(*args, **kwargs)

    def expiring(self):
        if self.status == "Delivered" or self.expired():
            return False
        today = date.today()
        try:
            if self.expiration_date <= today + timedelta(days=PRESCRIPTIONS_EXPIRING):
                return True
            else:
                return False
        except:
            return False

    def expired(self):
        if self.status == "Delivered":
            return False
        today = date.today()
        try:
            if self.expiration_date < today:
                return True
            else:
                return False
        except:
            return False

    def restore(self):
        self.is_deleted = False
        self.delete_date = None
        self.save()

    def delete(self, **kwargs):
        if not self.is_deleted:
            self.is_deleted = True
            self.delete_date = timezone.now()
            self.save()
        else:
            self.hard_delete()

    def hard_delete(self):
        super(Order, self).delete()
