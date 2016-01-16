from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    DeleteView)
from django.views.generic.edit import ModelFormMixin
from django.core.urlresolvers import reverse_lazy
from .models import Beer, Order, OrderItem

def index(request):
    context = {'nav_active': 'home'}
    return render(request, 'feer/index.html', context)

class BeerList(ListView):
    model = Beer

    def get_context_data(self, **kwargs):
        context = super(BeerList, self).get_context_data(**kwargs)
        context['nav_active'] = 'beers'
        return context

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

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        context['nav_active'] = 'orders'
        return context

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
    fields = ['beer', 'order_list', 'quantity', 'cost', 'participants', 'volume_per_participant']

class OrderItemUpdate(UpdateView):
    model = OrderItem
    fields = ['beer', 'order_list', 'quantity', 'cost', 'participants', 'volume_per_participant']

class OrderItemDelete(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('order_list')
