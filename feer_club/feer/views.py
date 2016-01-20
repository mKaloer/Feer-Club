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
import logging
logger = logging.getLogger(__name__)

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

def order_item_form_valid(self, form):
    # Subtract old price from order
    if form.instance.cost is not None:
        form.instance.order.cost -= form.instance.cost
    form.instance.cost = form.instance.beer.price * form.instance.quantity
    form.instance.volume_per_participant = 0
    # Save so that participants can be referenced
    form.save()
    num_of_participants = form.instance.participants.count()
    form.instance.volume_per_participant = (0 if num_of_participants == 0 else
        form.instance.beer.volume / num_of_participants)
    form.instance.order.cost += form.instance.cost
    form.instance.order.save()
    form.save()
    return HttpResponseRedirect(reverse_lazy('order_detail',
        kwargs={'pk': form.instance.order.pk}))

class OrderItemCreate(LoginRequiredMixin, CreateView):
    model = OrderItem
    fields = ['beer', 'order', 'quantity', 'participants', 'drink_date']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        return order_item_form_valid(self, form)

class OrderItemUpdate(LoginRequiredMixin, UpdateView):
    model = OrderItem
    fields = ['beer', 'order', 'quantity', 'participants', 'drink_date']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        return order_item_form_valid(self, form)

class OrderItemDelete(LoginRequiredMixin, DeleteView):
    model = OrderItem
    login_url = reverse_lazy('login')

    def delete(self, *args, **kwargs):
        order_item = self.get_object()
        order_item.order.cost -= order_item.cost
        order_item.order.save()
        return super().delete(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.order.pk})
