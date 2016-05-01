from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    DeleteView)
from django.views.generic.edit import ModelFormMixin
from django.core.urlresolvers import reverse_lazy
from django.core.signals import request_finished
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Beer, Order, OrderItem, Rating
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import date
from decimal import *
import logging
import math
logger = logging.getLogger(__name__)

def index(request):
    context = {'nav_active': 'home'}
    return render(request, 'feer/index.html', context)

@login_required(login_url=reverse_lazy('login'))
def profile(request):
    return render(request, 'feer/profile.html')

@login_required(login_url=reverse_lazy('login'))
def my_ratings(request):
    ratings = sorted(Rating.objects.filter(user=request.user),
            key=lambda r: r.index,
            reverse=True)
    context = {'ratings': ratings, 'nav_active': 'my_ratings'}
    return render(request, 'feer/my_ratings.html', context)

@login_required(login_url=reverse_lazy('login'))
def edit_my_participation(request, pk):
    order_item_id = request.POST['order_item_id']
    checked = request.POST['checked']
    order_item = OrderItem.objects.get(id=order_item_id)
    order = Order.objects.get(id=order_item.order.id)
    if order.updatable == False:
        return HttpResponseBadRequest('order is not updatable')

    if checked == 'true':
        order_item.participants.add(request.user)
    else:
        order_item.participants.remove(request.user)
    order_item.save()

    msg = 'success'
    return HttpResponse(msg)

@login_required(login_url=reverse_lazy('login'))
def edit_my_ratings(request):
    no_of_reviews = Rating.objects.filter(user=request.user).count()
    old_index = no_of_reviews - int(request.POST['old_index']) - 1
    new_index = no_of_reviews - int(request.POST['new_index']) - 1

    if old_index < new_index:
        ratings = Rating.objects.filter(user=request.user, index__gt=old_index,
                index__lte=new_index)
        moved_rating = Rating.objects.get(user=request.user, index=old_index)
        for r in ratings:
            r.index -= 1
            r.save()
        moved_rating.index = new_index
        moved_rating.save()
    else:
        ratings = Rating.objects.filter(user=request.user, index__gte=new_index,
                index__lt=old_index)
        moved_rating = Rating.objects.get(user=request.user, index=old_index)
        for r in ratings:
            r.index += 1
            r.save()
        moved_rating.index = new_index
        moved_rating.save()

    msg = 'success'
    return HttpResponse(msg)

class NonOverwritingUpdateView(UpdateView):
    """
    UpdateView subclass that ensures that the model has not been
    changed since load. If so, a validation error is shown.
    """
    def get(self, request, *args, **kwargs):
        # Save last update in session
        obj = self.get_object()
        obj_name = obj.__class__.__name__
        request.session["%s_%s_initial_updated" % (obj_name, obj.id)] = str(obj.updated)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        curr_obj = self.get_object()
        obj_name = curr_obj.__class__.__name__
        # Check if object has been updated since view loaded
        if (self.request.session["%s_%s_initial_updated" % (obj_name, curr_obj.id)] != str(curr_obj.updated)):
            # Show error
            form.add_error(None,
                           ValidationError(_('Error: Object modified since load'), code='modified'))
            return super().form_invalid(form)
        return super().form_valid(form)

class RatingCreate(LoginRequiredMixin, CreateView):
    model = Rating
    fields = ['beer', 'comment']
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        ratings = Rating.objects.filter(user=current_user)
        rated_beers = []
        for r in ratings:
            rated_beers.append(r.beer.id)
        beers = Beer.objects.exclude(id__in=rated_beers)
        context = super(RatingCreate, self).get_context_data(**kwargs)
        context['beers'] = beers
        return context

    def form_valid(self, form):
        current_user = self.request.user
        current_no_of_reviews = Rating.objects.filter(user=current_user).count()
        form.instance.user = current_user
        form.instance.index = current_no_of_reviews
        form.save()
        return HttpResponseRedirect(reverse_lazy('my_ratings'))

class RatingUpdate(LoginRequiredMixin, NonOverwritingUpdateView):
    model = Rating
    template_name_suffix = '_update_form'
    fields = ['comment']
    success_url = reverse_lazy('my_ratings')
    login_url = reverse_lazy('login')

class RatingDelete(LoginRequiredMixin, DeleteView):
    model = Rating
    success_url = reverse_lazy('my_ratings')
    login_url = reverse_lazy('login')

    def delete(self, *args, **kwargs):
        index = self.get_object().index
        current_user = self.request.user
        ratings_to_update = Rating.objects.filter(user=current_user,
                index__gt=index)
        for r in ratings_to_update:
            r.index -= 1
            r.save()
        return super().delete(*args, **kwargs)

class BeerList(LoginRequiredMixin, ListView):
    model = Beer
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        ratings = Rating.objects.filter(user=current_user)
        rated_beers = []
        for r in ratings:
            rated_beers.append(r.beer)
        context = super(BeerList, self).get_context_data(**kwargs)
        context['nav_active'] = 'beers'
        context['rated_beers'] = rated_beers
        return context

class BeerDetail(LoginRequiredMixin, DetailView):
    model = Beer
    login_url = reverse_lazy('login')

class BeerCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Beer
    fields = ['name', 'brewery', 'country', 'style', 'abv', 'ibu', 'volume',
              'purchase_url', 'price']
    login_url = reverse_lazy('login')
    permission_required = "feer.add_beer"

class BeerUpdate(LoginRequiredMixin, PermissionRequiredMixin, NonOverwritingUpdateView):
    model = Beer
    fields = ['name', 'brewery', 'country', 'style', 'abv', 'ibu', 'volume',
              'purchase_url', 'price']
    login_url = reverse_lazy('login')
    permission_required = "feer.change_beer"

class BeerDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Beer
    success_url = reverse_lazy('beer_list')
    login_url = reverse_lazy('login')
    permission_required = "feer.delete_beer"

class OrderList(LoginRequiredMixin, ListView):
    model = Order
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        context['nav_active'] = 'orders'
        orders = Order.objects.all()
        orders_shipped = {}
        for o in orders:
            orders_shipped[o] = True if o.order_date < date.today() else False
        context['orders_shipped'] = orders_shipped
        return context

class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        costs, emails = participant_information(self.object)
        costs = add_costs_equally(costs, self.object.remainding_balance)
        costs, shipping_cost_required = add_shipping_cost(costs, self.object.cost())

        context['costs'] = round_participant_costs(costs)
        context['emails'] = emails
        context['shipping_cost_required'] = shipping_cost_required
        return context

def add_shipping_cost(costs, order_cost):
    shipping_cost_required = False
    res = costs
    if order_cost < 500:
        shipping_cost_required = True
        res = add_costs_equally(costs, 49)
    return res, shipping_cost_required

def participant_information(order):
    items = OrderItem.objects.filter(order__id=order.id)
    costs = {}
    emails = {}
    for item in items:
        num_of_participants = item.participants.count()
        for p in item.participants.all():
            cost = item.cost() / num_of_participants
            if p.username in costs:
                costs[p.username] += cost
            else:
                costs[p.username] = cost
            if p.username not in emails:
                emails[p.username] = p.email
    return sorted(costs.items()), '; '.join(emails.values())

def round_participant_costs(costs):
    return list(map(lambda t: (t[0], math.ceil(t[1])), costs))

def add_costs_equally(costs, extra_cost):
    if len(costs) == 0:
        return costs
    r = extra_cost / len(costs)
    return list(map(lambda t: (t[0], t[1] + Decimal(r)), costs))

class OrderCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    fields = ['name', 'order_date', 'remainding_balance']
    login_url = reverse_lazy('login')
    permission_required = "feer.add_order"

    def form_valid(self, form):
        form.instance.cost = 0
        form.save()
        return HttpResponseRedirect(reverse_lazy('order_list'))

class OrderUpdate(LoginRequiredMixin, PermissionRequiredMixin, NonOverwritingUpdateView):
    model = Order
    fields = ['name', 'order_date', 'remainding_balance', 'updatable']
    login_url = reverse_lazy('login')
    permission_required = "feer.change_order"

class OrderDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
    login_url = reverse_lazy('login')
    permission_required = "feer.delete_order"

class OrderItemCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = OrderItem
    fields = ['beer', 'quantity', 'drink_date']
    login_url = reverse_lazy('login')
    permission_required = "feer.add_orderitem"

    def form_valid(self, form):
        order = Order.objects.get(pk=self.kwargs['pk'])
        if order.updatable == False:
            return HttpResponseBadRequest('order is not updatable')

        form.instance.order = order
        form.save()
        return HttpResponseRedirect(reverse_lazy('order_detail',
            kwargs={'pk': form.instance.order.pk}))

class OrderItemUpdate(LoginRequiredMixin, NonOverwritingUpdateView):
    model = OrderItem
    fields = ['beer', 'quantity', 'drink_date']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        order = Order.objects.get(id=self.object.order.id)
        if order.updatable == False:
            return HttpResponseBadRequest('order is not updatable')
        return HttpResponseRedirect(reverse_lazy('order_detail',
            kwargs={'pk': self.object.order.pk}))

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.order.pk})

class OrderItemDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = OrderItem
    login_url = reverse_lazy('login')
    permission_required = "feer.delete_orderitem"

    def form_valid(self, form):
        order = Order.objects.get(id=self.object.order.id)
        if order.updatable == False:
            return HttpResponseBadRequest('order is not updatable')
        return HttpResponseRedirect(reverse_lazy('order_detail',
            kwargs={'pk': self.object.order.pk}))

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.order.pk})
