from django.conf.urls import include, url
from .views import (BeerList, BeerDetail, BeerCreate, BeerUpdate, BeerDelete,
        OrderList, OrderDetail, OrderCreate, OrderUpdate, OrderDelete,
        OrderItemCreate, OrderItemDelete, OrderItemUpdate)

from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^orders/$', OrderList.as_view(), name='order_list'),
    url(r'^order/add/$', OrderCreate.as_view(), name='order_create'),
    url(r'^order/(?P<pk>[-\w]+)/$', OrderDetail.as_view(), name='order_detail'),
    url(r'^order/(?P<pk>[-\w]+)/additem/$', OrderItemCreate.as_view(), name='orderitem_create'),
    url(r'^order/(?P<pk>[-\w]+)/delete/$', OrderDelete.as_view(), name='order_delete'),
    url(r'^order/(?P<pk>[-\w]+)/edit/$', OrderUpdate.as_view(), name='order_update'),
    url(r'^order/(?P<order_pk>[-\w]+)/item/(?P<pk>[-\w]+)/delete/$', OrderItemDelete.as_view(), name='orderitem_delete'),
    url(r'^order/(?P<order_pk>[-\w]+)/item/(?P<pk>[-\w]+)/edit/$', OrderItemUpdate.as_view(), name='orderitem_update'),
    url(r'^beers/$', BeerList.as_view(), name='beer_list'),
    url(r'^beer/add/$', BeerCreate.as_view(), name='beer_create'),
    url(r'^beer/(?P<pk>[-\w]+)/$', BeerDetail.as_view(), name='beer_detail'),
    url(r'^beer/(?P<pk>[-\w]+)/delete/$', BeerDelete.as_view(), name='beer_delete'),
    url(r'^beer/(?P<pk>[-\w]+)/edit/$', BeerUpdate.as_view(), name='beer_update'),
    url(r'^profile/$', views.profile, name='user_profile'),
    url(r'^myratings/$', views.my_ratings, name='my_ratings'),
    url(r'^$', views.index, name='index'),
]
