from django.conf.urls import url
from .views import (BeerList, BeerDetail, BeerCreate, BeerUpdate, BeerDelete,
        OrderList, OrderCreate, OrderUpdate, OrderDelete)

from . import views

urlpatterns = [
    url(r'^orders/$', OrderList.as_view(), name='order_list'),
    url(r'^orders/add/$', OrderCreate.as_view(), name='order_create'),
    url(r'^orders/(?P<pk>[-\w]+)/delete/$', OrderDelete.as_view(), name='order_delete'),
    url(r'^orders/(?P<pk>[-\w]+)/edit/$', OrderUpdate.as_view(), name='order_update'),
    url(r'^beers/$', BeerList.as_view(), name='beer_list'),
    url(r'^beer/add/$', BeerCreate.as_view(), name='beer_create'),
    url(r'^beer/(?P<pk>[-\w]+)/delete/$', BeerDelete.as_view(), name='beer_delete'),
    url(r'^beer/(?P<pk>[-\w]+)/edit/$', BeerUpdate.as_view(), name='beer_update'),
    url(r'^beer/(?P<pk>[-\w]+)/$', BeerDetail.as_view(), name='beer_detail'),
    url(r'^$', views.index, name='index'),
]
