# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Customer(models.Model):
    CUSTOMER_STATE_PROSPECTIVE = 1
    CUSTOMER_STATE_CURRENT = 2
    CUSTOMER_STATE_NONACTIVE = 3
    CUSTOMER_STATE_CHOICES = (
        (CUSTOMER_STATE_PROSPECTIVE, "prospective"),
        (CUSTOMER_STATE_CURRENT, "current"),
        (CUSTOMER_STATE_NONACTIVE, "non-active")
    )
        
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=64, unique=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    state = models.IntegerField(choices=CUSTOMER_STATE_CHOICES,
                                 default=CUSTOMER_STATE_CURRENT)
    created_time = models.DateTimeField(auto_now=True)

    def display_name(self):
        if self.first_name:
            if self.last_name:
                return "%s, %s" % (self.last_name, self.first_name)
            else:
                return self.first_name
        else:
            return self.email

    def __str__(self):
        return self.display_name()


@python_2_unicode_compatible
class Note(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    updated_time = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        header_len = 32
        return self.content[:header_len]
