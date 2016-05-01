from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

class Beer(models.Model):
    name = models.CharField(max_length=512)
    brewery = models.CharField(max_length=512)
    country = models.CharField(max_length=512)
    style = models.CharField(max_length=512)
    abv = models.FloatField()
    ibu = models.IntegerField(null=True, blank=True)
    volume = models.IntegerField()
    purchase_url = models.URLField(max_length=512)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ratings = models.ManyToManyField(User, through="Rating")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('beer_detail', kwargs={'pk': self.pk})

class OrderItem(models.Model):
    beer = models.ForeignKey('Beer')
    order = models.ForeignKey('Order')
    quantity = models.IntegerField()
    participants = models.ManyToManyField(User)
    drink_date = models.DateField('drink date')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def volume_per_participant(self):
        num_of_parts = self.participants.count()
        if num_of_parts == 0:
            return 0
        else:
            return (self.beer.volume * self.quantity) / num_of_parts

    def participants_abbreviation(self):
        abbr = ''
        for user in self.participants.all():
            abbr += user.username + ', '
        return abbr.strip(', ')

    def cost(self):
        return self.beer.price * self.quantity

    def __str__(self):
        return str(self.quantity) + 'x ' + self.beer.name

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.order_list.pk})

class Order(models.Model):
    name = models.CharField(max_length=512)
    beers = models.ManyToManyField(Beer, through='OrderItem')
    order_date = models.DateField('order date')
    remainding_balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    cost_for_free_shipping = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    updatable = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def cost(self):
        return sum([i.cost() for i in self.orderitem_set.all()])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

class Rating(models.Model):
    class Meta:
        unique_together = ('beer', 'user')

    beer = models.ForeignKey(Beer)
    user = models.ForeignKey(User)
    index = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + " review of " + str(self.beer)
