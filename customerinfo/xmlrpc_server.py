# coding: utf-8

import logging
from django_xmlrpc.decorators import xmlrpc_func
from .models import *

logger = logging.getLogger('django.server')

# registered methods
@xmlrpc_func(returns='string', args=['string'])
def test_xmlrpc(text):
    """Simply returns the args passed to it as a string"""
    return "Here's a response! %s" % str(text)


