from django.conf.urls import patterns, url
from skipass import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^balance/$', views.user_balance, name='balance'),
        url(r'^balance/payment/$',views.payment, name='payment'),
         url(r'^balance/payment/charge_card/$',views.charge_card, name='payment')
        )
