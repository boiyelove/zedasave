from django.conf.urls import url
from. import views

app_name = 'zeraadmin'
urlpatterns = [
	url(r'^customers/$', views.customers, name='customer-list' ),
	url(r'^payments/$', views.payments, name='payment-list' ),


]