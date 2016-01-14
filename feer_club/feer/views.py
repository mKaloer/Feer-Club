from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    DeleteView)
from django.core.urlresolvers import reverse_lazy
from .models import Beer, Order

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

class OrderCreate(CreateView):
    model = Order
    fields = ['name', 'beers', 'order_date', 'cost']

class OrderUpdate(UpdateView):
    model = Order
    fields = ['name', 'beers', 'order_date', 'cost']

class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
