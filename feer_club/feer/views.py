from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    DeleteView)
from django.views.generic.edit import ModelFormMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Beer, Order, OrderItem

def index(request):
    context = {'nav_active': 'home'}
    return render(request, 'feer/index.html', context)

@login_required(login_url=reverse_lazy('login'))
def profile(request):
    return render(request, 'feer/profile.html')

class BeerList(LoginRequiredMixin, ListView):
    model = Beer
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(BeerList, self).get_context_data(**kwargs)
        context['nav_active'] = 'beers'
        return context

class BeerDetail(LoginRequiredMixin, DetailView):
    model = Beer
    login_url = reverse_lazy('login')

class BeerCreate(LoginRequiredMixin, CreateView):
    model = Beer
    fields = ['name', 'brewery', 'country', 'style', 'abv', 'ibu', 'volume',
              'purchase_url', 'price']
    login_url = reverse_lazy('login')

class BeerUpdate(LoginRequiredMixin, UpdateView):
    model = Beer
    fields = ['name', 'brewery', 'country', 'style', 'abv', 'ibu', 'volume',
              'purchase_url', 'price']
    login_url = reverse_lazy('login')

class BeerDelete(LoginRequiredMixin, DeleteView):
    model = Beer
    success_url = reverse_lazy('beer_list')
    login_url = reverse_lazy('login')

class OrderList(LoginRequiredMixin, ListView):
    model = Order
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        context['nav_active'] = 'orders'
        return context

class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    login_url = reverse_lazy('login')

class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['name', 'order_date']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.cost = 0
        form.save()
        return HttpResponseRedirect(reverse_lazy('order_list'))

class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    fields = ['name', 'order_date']
    login_url = reverse_lazy('login')

class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
    login_url = reverse_lazy('login')

class OrderItemCreate(LoginRequiredMixin, CreateView):
    model = OrderItem
    fields = ['beer', 'order', 'quantity', 'participants', 'drink_date']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.cost = form.instance.beer.price * form.instance.quantity
        form.instance.volume_per_participant = form.instance.beer.volume / form.instance.participants
        form.instance.order.cost += form.instance.cost
        form.instance.order.save()
        form.save()
        return HttpResponseRedirect(reverse_lazy('order_detail', kwargs={'pk': form.instance.order.pk}))

class OrderItemUpdate(LoginRequiredMixin, UpdateView):
    model = OrderItem
    fields = ['beer', 'order', 'quantity', 'participants', 'drink_date']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.cost = form.instance.beer.price * form.instance.quantity
        form.instance.volume_per_participant = form.instance.beer.volume / form.instance.participants
        form.instance.order.cost += form.instance.cost
        form.instance.order.save()
        form.save()
        return HttpResponseRedirect(reverse_lazy('order_detail', kwargs={'pk': form.instance.order.pk}))

class OrderItemDelete(LoginRequiredMixin, DeleteView):
    model = OrderItem
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.order.pk})
