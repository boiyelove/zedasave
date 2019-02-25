from django.conf.urls import url
from . import views


app_name='zerasaver'
urlpatterns = [
	url(r'^add/$', views.ZeraPlanCV.as_view(), name='create-zeraplan'),
	url(r'^(?P<pk>\d+)/edit/$', views.ZeraPlanUV.as_view(), name='edit-zeraplan'),

	url(r'^userplan/add/$', views.UserPlanCV.as_view(), name='create-userplan'),
	url(r'^userplan/(?P<pk>\d+)/edit/$', views.UserPlanUV.as_view(), name='edit-userplan'),
	url(r'^transaction/complete/$', views.PPaymentView.as_view(), name='complete-transaction'),
	url(r'^transaction/check/(?P<ref_code>[\w+]*)/(?P<format>[1-3])/$', views.CheckTransaction.as_view(), name='check-transaction'),
	url(r'^withdrawals/$', views.WithdrawalsLV.as_view(), name='withdrawals-list'),
	url(r'^quicksave/$', views.QuickSaveFV.as_view(), name='quick-save'),
	url(r'^subscriptions/$', views.SubscriptionsLV.as_view(), name='list-subscriptions'),
	url(r'^subscriptions/status/$', views.SubscriptionsV.as_view(), name='subscription-status'),
	]