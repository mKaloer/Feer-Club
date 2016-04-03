from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
    DeleteView)
from django.views.generic.edit import ModelFormMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Beer, Order, OrderItem, Rating
from datetime import date
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

class RatingUpdate(LoginRequiredMixin, UpdateView):
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
        context['costs'] = round_participant_costs(costs)
        context['emails'] = emails
        return context

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
    fields = ['beer', 'quantity', 'drink_date']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['pk'])
        return HttpResponseRedirect(reverse_lazy('order_detail',
            kwargs={'pk': form.instance.order.pk}))

class OrderItemUpdate(LoginRequiredMixin, UpdateView):
    model = OrderItem
    fields = ['beer', 'quantity', 'drink_date']
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.order.pk})

class OrderItemDelete(LoginRequiredMixin, DeleteView):
    model = OrderItem
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.order.pk})
