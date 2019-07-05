# coding: utf-8

from django.contrib import admin

from .models import Customer, Note

admin.site.register(Customer)
admin.site.register(Note)
