from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

class Beer(models.Model):
    name = models.CharField(max_length=512)
    brewery = models.CharField(max_length=512)
    country = models.CharField(max_length=512)
    style = models.CharField(max_length=512)
    abv = models.FloatField()
    ibu = models.IntegerField()
    volume = models.IntegerField()
    purchase_url = models.URLField(max_length=512)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('beer_detail', kwargs={'pk': self.pk})

class OrderItem(models.Model):
    beer = models.ForeignKey('Beer')
    order = models.ForeignKey('Order')
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    participants = models.IntegerField()
    volume_per_participant = models.FloatField()

    def __str__(self):
        return str(self.quantity) + 'x ' + self.beer.name

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.order_list.pk})

class Order(models.Model):
    name = models.CharField(max_length=512)
    beers = models.ManyToManyField(Beer, through='OrderItem')
    order_date = models.DateField('order date')
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})
