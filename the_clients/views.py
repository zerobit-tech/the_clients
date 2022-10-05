from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from the_user.decorators import otp_required, must_be,change_password_required
from the_user.initial_groups import CUSTOMER_CARE_SUPERVISER, CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER
from the_user.utils import user_is

from the_system.utils.paginator import get_paginator

from .models import Client
from .forms import ClientForm, ClientUpdateForm


import logging
logger = logging.getLogger('ilogger')

# Create your views here.


# -------------------------------------------------------------
#
# -------------------------------------------------------------
@login_required
@must_be(group_name=CUSTOMER_CARE_SUPERVISER)
@otp_required
@change_password_required
# @cache_page(60 * 10)
def list_clients(request):
    if hasattr(request,'search_value'):
        clients_all = Client.objects.filter(
            name__icontains=request.search_value.lower())
    else:
        clients_all = Client.objects.all()

    page_number, clients = get_paginator(request, clients_all)

    context = {"clients": clients, "page": page_number}
    return render(request, 'the_clients/list.html', context)


# -------------------------------------------------------------
#
# -------------------------------------------------------------
@login_required
@must_be(group_name=CUSTOMER_CARE_SUPERVISER)
@otp_required
@change_password_required
def add_client(request):
    add_form = ClientForm()
    if request.method == "POST":
        add_form = ClientForm(data=request.POST)
        if add_form.is_valid():
            add_form.save()
            if hasattr(request,'capture_user_activity'):
                request.capture_user_activity.send(sender='the_client', request=request, target=add_form.instance,
                                              message="New client {} created".format(add_form.instance.user))

            messages.success(request, _(f"New client {add_form.instance.user} created successfully"))
            #cache.delete(reverse('the_clients:list'))
            return redirect("the_clients:list")

    context = {"add_form": add_form, }
    return render(request, 'the_clients/add.html', context)


# -------------------------------------------------------------
#
# -------------------------------------------------------------
@login_required
@must_be(group_name=CUSTOMER_CARE_SUPERVISER)
@otp_required
@change_password_required
def update_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client_form = ClientUpdateForm(request.POST or None, instance=client)
    if request.method == "POST":
        if client_form.is_valid():
            if hasattr(request,'capture_user_activity'):
                request.capture_user_activity.send(sender='the_client', request=request, target=client,
                                              message="Client {} updated".format(client.user))
            client_data = client_form.cleaned_data
          
            client.active = client_data["active"]
       
            client.save()
            #cache.delete(reverse('the_clients:list'))
            messages.success(request, _(f"Client {client.user} updated successfully"))

            return redirect("the_clients:display", pk=client.pk)

    context = {"form": client_form,"client_to_update":client }
    return render(request, 'the_clients/update.html', context)

# -------------------------------------------------------------
#
# -------------------------------------------------------------
@login_required
@must_be(group_name=CUSTOMER_CARE_SUPERVISER)
@otp_required
@change_password_required
# @cache_page(60 * 10)
def display_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    context = {"client": client, }
    return render(request, 'the_clients/display.html', context)