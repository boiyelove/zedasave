from django.shortcuts import render, Http404
from djpaystack.customer import Customer
from djpaystack.transaction import Transactions


# Create your views here.

def customers(request):
	# if not request.user.is_staff:
	# 	raise Http404
	customers = Customer().list_all()
	context = {}
	context['pcustomers'] = customers
	template = 'zerasaveadmin/customer_list.html'
	return render(request, template,  context)

def payments(request):
	# if not request.user.is_staff:
	# 	raise Http404
	transactions = Transactions().list_all()
	context = {}
	context['transactions'] = transactions
	template = 'zerasaveadmin/transaction_list.html'
	return render(request, template,  context)