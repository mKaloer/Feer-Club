from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    DeleteView)
from django.views.generic.edit import ModelFormMixin
from django.core.urlresolvers import reverse_lazy
from .models import Beer, Order, OrderItem

def index(request):
    return render(request, 'feer/index.html')

class BeerList(ListView):
    model = Beer

class BeerDetail(DetailView):
    model = Beer

class BeerCreate(CreateView):
    model = Beer
    fields = ['name', 'brewery', 'country', 'style', 'abv', 'ibu', 'volume',
              'purchase_url', 'price']

class BeerUpdate(UpdateView):
    model = Beer
    fields = ['name', 'brewery', 'country', 'style', 'abv', 'ibu', 'volume',
              'purchase_url', 'price']

class BeerDelete(DeleteView):
    model = Beer
    success_url = reverse_lazy('beer_list')

class OrderList(ListView):
    model = Order

class OrderDetail(DetailView):
    model = Order

class OrderCreate(CreateView):
    model = Order
    fields = ['name', 'order_date', 'cost']

class OrderUpdate(UpdateView):
    model = Order
    fields = ['name', 'order_date', 'cost']

class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')

class OrderItemCreate(CreateView):
    model = OrderItem
    fields = ['beer', 'order_list', 'quantity', 'participants', 'volume_per_participant']

class OrderItemUpdate(UpdateView):
    model = OrderItem
    fields = ['beer', 'order_list', 'quantity', 'participants', 'volume_per_participant']

class OrderItemDelete(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('order_list')
