# coding: utf-8

import re
import requests
import logging
from datetime import datetime as dt

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import date
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404

from .models import *
from .templatetags import myfilters
from . import conf

logger = logging.getLogger('django.server')

@login_required
def show_customerlist(request):
    context = {
        'title': 'CustomerList',
    }
    output = render(request, 'customerlist.html', context)
    return output


@login_required
def show_customer(request, cid):
    customer = get_object_or_404(Customer, pk=cid)
    context = {
        'title': 'CustomerInfo',
        'customer': customer,
        'state_choices': Customer.CUSTOMER_STATE_CHOICES,
        'time_fmt': conf.TIME_STRFMT_DJGTAG,
    }
    output = render(request, 'customer.html', context)
    return output


@login_required
def ajax_clst_search(request):
    if request.method != 'POST':
        return HttpResponse(status=500)

    # query string
    qstr = request.POST.get('qstr').strip()
    # sort column
    sort_col = request.POST.get('sort_col')
    # sort direction
    sort_dir = request.POST.get('sort_dir')
    # if no query condition, show all records
    cqs = Customer.objects.all()
    
    invalid_query = False
    if qstr:
        # search by id
        m = re.match(r'^\d+$', qstr)
        if m:
            cqs = cqs.filter(pk=int(qstr))
        else:
            # search by email
            m = re.search(r'[\.@]', qstr)
            if m:
                cqs = cqs.filter(email__icontains=qstr)
            else:
                # search by either name or email
                m = re.match(r'^[a-zA-Z]\w*$', qstr)
                if m:
                    query = Q(first_name__icontains=qstr)
                    query.add(Q(last_name__icontains=qstr), Q.OR)
                    query.add(Q(email__icontains=qstr), Q.OR)
                    cqs = cqs.filter(query)
                else:
                    # search by phone
                    m = re.match(r'^[0-9()\- ]{6,}$', qstr)
                    if m:
                        cqs = cqs.filter(phone__icontains=qstr)
                    else:
                        invalid_query = True

    customer_data = []
    if not invalid_query:
        # set sorting 
        cqs = cqs.order_by("%s%s" % (sort_dir, sort_col))
        # refactor the data structure of customer for template
        for c in cqs:
            customer_data.append({
                'img': myfilters.uname_display(c, True),
                'id': c.id,
                'first_name': c.first_name,
                'last_name': c.last_name,
                'state': c.get_state_display(),
                'email': c.email,
                'phone': c.phone,
                'created': date(c.created_time, conf.TIME_STRFMT_DJGTAG_S),
            })

    rsp_data = {
        'colcnt': 7,
    }
    rsp_data['customers'] = customer_data
    rsp_data['status'] = True
    return JsonResponse(rsp_data)


@login_required
def ajax_note_action(request):
    if request.method != 'POST':
        return HttpResponse(status=500)

    action_type = request.POST.get('form_action_type')
    # customer id
    cid = int(request.POST.get('form_cid'))
    # note id
    nid = request.POST.get('form_nid')
    if nid:
        nid = int(nid)
    note_text = request.POST.get('form_note_text')

    if action_type == 'add':
        note = Note(author_id=request.user.id,
                    customer_id=int(cid),
                    text=note_text)
        # create a note in database
        note.save()
    elif action_type == 'edit':
        # update note text in database
        Note.objects.filter(pk=nid).update(text=note_text,
                                           updated_time=dt.now())
    elif action_type == 'delete':
        # delete note from database
        Note.objects.filter(pk=nid).delete()

    # query all notes associated with this customer, 
    # and ordered by updated_time in descending so
    # that the latest note is on the top
    nqs = Note.objects.select_related(
            'author').filter(customer_id=cid).order_by('-updated_time')

    # refactor the data of notes for the template
    note_data = []
    for n in nqs:
        note_data.append({
            'id': n.id,
            'author_id': n.author.id,
            'author_email': n.author.email,
            'author_img': myfilters.uname_display(n.author, True),
            'author_name': n.author.username,
            'updated': date(n.updated_time, conf.TIME_STRFMT_DJGTAG),
            'text': mark_safe(n.text),
        })

    rsp_data = {
        'notes': note_data,
        'status': True,
    }
    return JsonResponse(rsp_data)


@login_required
def ajax_change_state(request):
    if request.method != 'POST':
        return HttpResponse(status=500)

    # customer id
    cid = int(request.POST.get('form_cid'))
    state = int(request.POST.get('form_state'))

    Customer.objects.filter(pk=cid).update(state=state)

    rsp_data = {
        'status': True,
    }
    return JsonResponse(rsp_data)
