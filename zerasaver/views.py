import json
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from djpaystack.plan import Plan
from djpaystack.subscription import Subscription
from djpaystack.transaction import Transactions
from .forms import ZeraPlanForm, UserSavingsForm, QuickSaveForm
from .models import ZeraPlan, UserSavingsPlan, Withdrawals, USubscriptions
from .utils import verify_transaction, INTERVALLIST

# Create your views here.
class AjaxableResponseMixin(object):
	def render_to_json_response(self, context, **kwargs):
		data = json.dumps(context)
		kwargs['content_type'] ='application/json'
		return HttpResponse(data, **kwargs)

	def form_invalid(self, form):
		response = super(AjaxableResponseMixin, self).form_invalid(form)
		if self.request.is_ajax():
			return self.render_to_json_response(form.errors, status=400)
		return response

	def form_valid(self, form):
		response = super(AjaxableResponseMixin, self).form_valid(form)
		if self.request.is_ajax():
			data = {
			'pk': self.object.pk
			}
			return self.render_to_json_response(data)
		return response

class AnyForm:
	page_title = ''
	form_title = ''
	form_action = '.'
	form_method = 'POST'
	form_value = 'Save'
	error_message = 'Please check the details you provided'

	def get_context_data(self, *args, **kwargs):
		context = kwargs.get('context', {})
		context.update({'page_title' : self.page_title,
		'form_title': self.form_title,
		"form_action": self.form_action,
		"form_method": self.form_method,
		"form_value": self.form_value,
		'error_message': self.error_message,
		})
		return super(AnyForm, self).get_context_data(*args, **kwargs, context=context)

class CreateForm(AnyForm):
	page_title = 'Create'
	form_title = 'Create'
	form_action = '.'
	form_method = 'POST'
	form_value = 'Create'

class EditForm(AnyForm):
	page_title = 'Update'
	form_title = 'Update'
	form_action = '.'
	form_method = 'POST'
	form_value = 'Update'



class ZeraPlanEdit:
	form_class = ZeraPlanForm
	template_name = 'accounts/form.html'


class UserPlanEdit:
	form_class = UserSavingsForm
	template_name = 'zerasaver/create_plan.html'



class ZeraPlanCV(ZeraPlanEdit, CreateForm, CreateView):
	success_url = '/'

class ZeraPlanUV(ZeraPlanEdit, EditForm, UpdateView):
	pass


class ZeraPlanLV(ListView):
	model = ZeraPlan
	template_name = "accounts/form.html"


class UserPlanCV(UserPlanEdit, UpdateView):
	success_url = reverse_lazy('zerasaver:complete-transaction')
	page_title = 'Create Savings Plan'
	form_title = ''
	form_action = '.'
	form_method = 'POST'
	form_value = 'Save'
	error_message = 'Please check the details you provided'


	def get_context_data(self, *args, **kwargs):
		context = kwargs.get('context', {})
		context.update({'page_title' : self.page_title,
		'form_title': self.form_title,
		"form_action": self.form_action,
		"form_method": self.form_method,
		"form_value": self.form_value,
		'error_message': self.error_message,
		})
		return context

	def form_valid(self, form):
		uplan = self.get_object()
		print('week',form.instance.day_of_week)
		print('month', form.instance.day_of_month)
		print('deposit_time', form.instance.deposit_time)
		print('deposit_amount', form.instance.deposit_amount)
		
		if uplan.has_active_subscription():
			uplan.unsubscribe()

		try:
			form.instance.plan = ZeraPlan.objects.get(amount=form.instance.deposit_amount*100,
				frequency=form.instance.frequency)
		except:
			if form.instance.frequency == 1:
				name = 'DSP-'
				desc = 'Daily'
			if form.instance.frequency == 2:
				name = 'WSP-'
				desc = 'Weekly'
			if form.instance.frequency == 3:
				name = 'MSP-'
				desc = 'Monthly'
			name += str(form.instance.deposit_amount)
			desc = '%s Savings Plan for %s naira' % (desc, str(form.instance.deposit_amount))
			p = Plan()
			plan = p.create(name=name,
				amount = (form.instance.deposit_amount*100),
				interval=INTERVALLIST[form.instance.frequency],
				description=desc)
			form.instance.plan = ZeraPlan.objects.create(name= name, 
				amount=(form.instance.deposit_amount*100), 
				frequency=form.instance.frequency, 
				description = desc,
				pplan_code = plan['plan_code'],
				pplan_id = plan['id'])
		return super(UserPlanCV, self).form_valid(form)
		

	# def form_invalid(self, form):
	# 	print(form.errors)
	# 	return super(UserPlanCV, self).form_invalid(form)

	def get_object(self):
		obj, created = UserSavingsPlan.objects.get_or_create(user=self.request.user)
		return obj

class UserPlanUV(EditForm, UpdateView, UserPlanEdit):
	pass



class PPaymentView(TemplateView):
	template_name = 'zerasaver/paystackpayment.html'

	def dispatch(self, request, *args, **kwargs):
		try:
			myplan = UserSavingsPlan.objects.get(user=self.request.user)
			if myplan.auth:
				myplan.subscribe()
				messages.add_message(request, messages.SUCCESS, 'Your subscription was updated')
				return HttpResponseRedirect(reverse_lazy('accounts:dashboard'))
			#kwargs['myplan'] = myplan
			plan_data = {}
			plan_data['amount'] = myplan.deposit_amount * 100
			plan_data['invoice_limit'] = myplan.target
			plan_data['plan_code'] = myplan.plan.pplan_code
			kwargs['plan_data'] = plan_data
		except UserSavingsPlan.DoesNotExist:
			pass
		return super(PPaymentView, self).dispatch(request, *args, **kwargs)


class CheckTransaction(View):
	def get(self, request, *args, **kwargs):
		refcode = kwargs.get('ref_code', '')
		formatt = kwargs.get('format', 1)
		uplan = UserSavingsPlan.objects.get(user = request.user)
		transaction = Transactions()
		if transaction.verify_by_customer(reference_code=refcode,
			plan_code=uplan.plan.pplan_code, email=request.user.email):
			if uplan.pcus_code == None or uplan.pcus_id == None:
				customer = transaction.get_customer()
				uplan.pcus_code = customer['customer_code']
				uplan.pcus_id = customer['id']
				uplan.save()
				uplan.subscribe()

		#if verify_transaction(ref_code=refcode, plan_code=uplan.plan.pplan_code, email=request.user.email):
			return HttpResponse('Hello World ' + refcode + str(formatt), status=200)
		else:
			return HttpResponse(status=204)

class WithdrawalsLV(ListView):
	model = Withdrawals
	template_name = 'zerasaver/withdrawal_list.html'
	context_object_name = 'withdrawal_list'


class QuickSaveFV(FormView):
	form_class = QuickSaveForm
	template_name = 'zerasaver/quicksave.html'
	success_url = reverse_lazy('accounts:dashboard')

	def dispatch(self, *args, **kwargs):
		uplan = UserSavingsPlan.objects.get(user = self.request.user)
		if uplan.has_auth:
			return super(QuickSaveFV, self).dispatch(*args, **kwargs)
		else:
			return PPaymentView.as_view()(self.request)


		
	def form_valid(self, form):
		return super(QuickSaveFV, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		new_context = {'page_title' : 'Bank Account Details',
		'form_title': 'QuickSave',
		"form_action": reverse_lazy('zerasaver:quick-save'),
		"form_method": "post",
		"form_value": "Quickly Save this Amount Now",
		'error_message': "Please check the details you provided",
		}
		context = super(QuickSaveFV, self).get_context_data(*args, **kwargs)
		context.update(new_context)
		return context

class SubscriptionsLV(ListView):
	model = USubscriptions
	context_object_name = 'subscription_list'
	template_name='subscription_list.html'

class SubscriptionsV(View):
	def get(self, request, *args, **kwargs):
		status = request.GET.get('status', None)
		if request.is_ajax():
			if status == 'pause':
				Subscription.pause()
			elif status == 'stop':
				Subscription.stop()
			return HttpResponse('True')
		else:
			raise Http404