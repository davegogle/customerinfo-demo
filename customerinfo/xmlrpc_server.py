# coding: utf-8

import sys
import logging
from django_xmlrpc.decorators import xmlrpc_func
from django.core.exceptions import ObjectDoesNotExist
from .models import Customer

logger = logging.getLogger('django.server')

def myself():
    """Get the caller function's name """
    return sys._getframe(1).f_code.co_name


# registered methods
@xmlrpc_func(returns='string', args=['string'])
def test_xmlrpc(text):
    """Simply returns the args passed to it as a string"""
    return "Here's a response! %s" % str(text)


@xmlrpc_func(returns=['boolean', 'string', 'int'], args=['struct'])
def create_or_update_customer(customer_info):
    """ Create or update customer data in database. The behavior is the same
        as save(), i.e. if 'id' field is specified, data would be updated, 
        otherwise a new record would be created in database. Make sure the
        input data's name and type should be consistent with ones defined in
        models.py 

        Parameters:
            customer_info, struct: customer information

        Returns:
            boolean:               if the function executes successfully
            string:                error message
            int:                   created customer id
    """

    # initialize return values
    rv = [True, '', 0]

    myname = myself()
    model_fields = [ f.name for f in Customer._meta.fields ]
    field_data = {}
    # check if the key of customer_info is one
    # of the model fields, drop it if it isn't
    for k in customer_info.keys():
        if k in model_fields:
            field_data[k] = customer_info[k]
        else:
            logger.warn("%s: ingored invalid field %s" % (myname, k))

    try:
        customer = Customer(**field_data)
        customer.save()
        rv[2] = customer.id
    except Exception as e:
        rv[0] = False
        rv[1] = str(e)
        logger.error("%s: %s" % (myname, rv[1]))

    return rv


@xmlrpc_func(returns=['boolean', 'string', 'struct'], args=['int'])
def get_customer(customer_id):
    """ Get the customer information from database

        Parameters:
            customer_id, int: customer identifer

        Returns:
            boolean:          if the function executes successfully
            string:           error message
            struct:           customer information
    """
    # initialize return values
    rv = [True, '', {}]

    myname = myself()
    model_fields = [ f.name for f in Customer._meta.fields ]
    try:
        customer = Customer.objects.get(pk=customer_id)
        rv[2] = {
            'id': customer.id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone': customer.phone,
            'state': customer.state,
            'created_time': customer.created_time,
        }
    except ObjectDoesNotExist as e:
        rv[0] = False
        rv[1] = str(e)
        logger.error("%s: %s" % (myname, rv[1]))

    logger.info(rv)
    return rv
