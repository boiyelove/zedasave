from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from djpaystack.subscription import Subscription
from djpaystack.customer import Customer
from djpaystack.transaction import Transactions
from djpaystack.plan import Plan
from webcore.models import TimestampedModel
from .utils import DAYS_OF_MONTH, DAY_OF_WEEK, INTERVAL, TIME_OF_DAY


# Create your models here.

FREQUENCY = (
	(1 , 'daily'),
	(2, 'weekly'),
	(3, 'monthly'), 
	)


class WithdrawalsManager(models.Manager):
	def check_available_withdrawals(self, user):
		pass

	def get_total_withdrawals(self, user):
		total = self.filter(user=user).aggregate(total_amount=models.Sum('amount'))
		return total['total_amount']

	
class ZeraPlanManager(models.Manager):
	def create_from_paystack(self):
		p = Plan()
		plans = p.list_all()
		newplans = []
		for plan in plans:
			try:
				self.get(amount=plan['amount'], interval=INTERVAL[plan['interval']])
			except:
				newplan = self.create(name=plan['name'],
					amount=plan['amount'],
					frequency =INTERVAL[plan['interval']],
					description = plan['description'],
					pplan_id = plan['id'],
					pplan_code = plan['plan_code']
					)
				newplans.append(newplan)
		return newplans







class ZeraPlan(TimestampedModel):
	name = models.CharField(max_length=50)
	description = models.TextField(null=True)
	amount = models.PositiveIntegerField(default=100)
	frequency = models.IntegerField(default=1, choices=FREQUENCY)
	currency = models.CharField(max_length=3, default='NGN')
	send_invoices = models.BooleanField(default=True)
	send_sms = models.BooleanField(default=True)
	hosted_page = models.BooleanField(default=False)
	hosted_page_url = models.URLField(null=True)
	hosted_page_summary = models.TextField()
	pplan_id = models.PositiveIntegerField(null=True)
	pplan_code = models.CharField(max_length = 100, null=True)

	objects = ZeraPlanManager()

	def __str__(self):
		return self.name

	def update_subscriptions_list(self):
		status = False
		plan = Plan(code=self.pplan_code)
		plan = plan.get_data()
		plan = plan['data']
		for sub in plan['subscriptions']:
			 oneplan = ZeraPlan.objects.get(pplan_code = plan['plan_code'])
			 onecus = Customer(id=sub['customer'])
			 onecus = onecus.get_data()
			 try:
			 	u = User.objects.get(email=onecus['email'])
			 except User.DoesNotExist:
			 	u = User.objects.create_user(email=onecus['email'], username=onecus['email'])
			 if sub['status'] == "active":
			 	status=True
			 	try:
			 		obj = USubscriptions.objects.get(psub_id=sub['id'])
			 		if not obj.active:
			 			obj.active = True
			 			if not obj.psub_token:
			 				psub_token = sub['email_token']
			 			obj.save()
			 	except USubscriptions.DoesNotExist:
			 		obj = USubscriptions.objects.create(user=u,plan=self, psub_id=sub['id'],psub_code=sub['subscription_code'],psub_token = sub['email_token'], active = status)

			 if status:
			 	uplan = u.usersavingsplan
			 	uplan.active_sub = obj
			 	uplan.save()


class UserSavingsPlan(TimestampedModel):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	plan = models.ForeignKey(ZeraPlan, null=True)
	pcus_code = models.CharField(max_length=100, editable=False, null=True)
	pcus_id = models.PositiveIntegerField(editable=False, null=True)
	active_sub = models.ForeignKey('USubscriptions', null=True, blank=True)
	has_auth = models.BooleanField(default=False, blank=True)
	auth = models.CharField(max_length=50, null=True, editable=False)
	frequency = models.IntegerField(default=1, choices=FREQUENCY)
	day_of_month =  models.IntegerField(default=1, choices = DAYS_OF_MONTH[:28], null=True, blank=False)
	day_of_week =  models.IntegerField(default=1, choices=DAY_OF_WEEK, null=True, blank=False)
	deposit_amount = models.PositiveIntegerField(default = 0, blank=False)
	target = models.PositiveIntegerField(default = 0, blank=False)
	start_date = models.DateTimeField(null=True, blank=True)
	target_date = models.DateTimeField(null=True, blank=True)
	deposit_time = models.IntegerField(default=1, null=True, blank=False)

	def __str__(self):
		return str(self.plan) + ' ' + str(self.user)


	def get_savings(self):
		return None

	def status(self, mode):
		mysub = Subscription(plan_code = self.plan.pplan_id, customer_id = self.pcus_id)
		if mode ==True:
			mySub.enable(token=self.psub_token)
		else:
			mysub.disable(token=self.psub_token)
		return True

	def stop(self):
		self.status(False)
		self.plan = None
		self.psub_id = self.psub_code = None
		self.save()

	def unsubscribe(self):
		if self.active_sub:
			current_sub = self.active_sub
			current_sub.disable()			
			self.active_sub = None
			self.deposit_amount = 0
			self.target = 0
			self.start_date = None
			self.target_date = None
			self.save()
		subs = USubscriptions.objects.filter(user = self.user)
		for sub in subs:
			sub.disable()
		
	def pause(self):
		if self.active_sub:
			self.active_sub.diasble()

	def play(self):
		if self.active_sub:
			self.active_sub.enable()

	def subscribe(self):
		self.unsubscribe()
		mySub = None
		hr = int(TIME_OF_DAY[self.deposit_time].split('.')[0])
		mn = int(TIME_OF_DAY[self.deposit_time].split('.')[1])
		start_date = timezone.now().replace(hour=hr, minute=mn)
		if self.frequency == 1:
			if timezone.now() >= start_date:
				start_date = start_date + timedelta(days=1)
			target_date = start_date + timedelta(days=self.target)
		elif self.frequency == 2:
			if self.day_of_week <= start_date.isoweekday():
				start_date = (start_date  - timedelta(days=self.day_of_week)) +  timedelta(days=7)
				target_date = start_date + timedelta(days = 7 * self.target)
		elif self.frequency == 3:
			start_date = start_date.replace(day=self.day_of_month)
			if timezone.now() > start_date:
				start_date = start_date + relativedelta(months=1)
			target_date = start_date + relativedelta(months=self.target)
		self.target_date = target_date

		if self.has_auth:
			try:
				mySub = USubscriptions.objects.get(user=self.user, plan=self.plan)
				mySub.enable()
			except USubscriptions.DoesNotExist:
				new_sub = Subscription()
				new_sub = new_sub.create(plan_code=self.plan.pplan_code, email=self.user.email, 
					start_date=start_date.isoformat(), invoice_limit=self.target)
				if new_sub:	
					try:	
						plan = new_sub['plan']
						plan = ZeraPlan.objects.get(pplan_id = plan)

						mySub = USubscriptions.objects.create(user=self.user,
							plan = plan,
							psub_code = new_sub['subscription_code'],
							psub_id = new_sub['id'],
							psub_token = new_sub['email_token'])
						self.active_sub = mySub
						self.save()
					except KeyError:
						self.plan.update_subscriptions_list()



	def current_savings(self):
		transactions = Transactions()
		total = transactions.user_totals(self.pcus_id)
		totalwithdrawn = WithdrawalRequest.objects.get_total_withdrawals(user=self.user)
		if totalwithdrawn:
			total = total - totalwithdrawn
		return total

	def pull_customer_data(self):
		customer_data = Customer()
		customer_data = customer_data.create(self.user.email,
			self.user.first_name,
			lastname = self.user.last_name,
			phone = self.user.userprofile.phone)
		if customer_data:
			self.pcus_code = customer_data[1]
			self.pcus_id = customer_data[0]
			customer = Customer(id=customer_data[0])
			customer = customer.get_data()
			print('customer is', customer)
			if customer['authorizations']:
				self.has_auth = True
				self.auth = customer['authorizations'][0]
			self.save()
			return self
		return False

	def update_auth(self):
		customer = Customer(id=self.pcus_id)
		if customer['authorizations']:
			self.has_auth = True
			self.save()

	def verify_my_transaction(self, reference_code):
		transaction = Transaction()
		return transaction.verify_by_customer(plan_code = self.plan.pplan_code,
			email=self.user.email, 
			customer_code = self.pcus_code, 
			customer_id=self.pcus_id)

	def has_active_subscription(self):
		if USubscriptions.objects.filter(user=self.user, active=True).exists():
			return True
		else:
			return False

	def has_auth(self):
		if self.has_auth: return True
		return False

class WithdrawalAcc(TimestampedModel):
	account_name = models.CharField(max_length = 100)
	account_number = models.PositiveIntegerField(default=0)
	bank_name = models.SlugField()

	def __str__(self):
		return('%s -  %s' % (self.account_number, self.bank_name))

class WithdrawalRequest(TimestampedModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	amount = models.PositiveIntegerField()
	bank_details = models.ForeignKey(WithdrawalAcc)

	objects = WithdrawalsManager()

	def __str__(self):
		return ('%s -  %s' %  (self.user, self.amount))

class Withdrawals(TimestampedModel):
	request = models.OneToOneField(WithdrawalRequest)

class USubscriptions(TimestampedModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
	plan = models.ForeignKey(ZeraPlan)
	target = models.PositiveIntegerField(default=2)
	psub_id = models.PositiveIntegerField(editable=False, unique=True)
	psub_code = models.CharField(max_length=100, editable=False, unique=True)
	psub_token = models.CharField(max_length=100, editable=False, unique=True)
	active = models.BooleanField(default = True)

	def enable(self, mode=True):
		# new_sub = Subscription(plan_code=self.plan.pplan_code, email=self.user.email)
		# self.psub_code = new_sub['subscription_code']
		# self.psub_id = new_sub['id']
		# self.psub_token = new_sub['email_token']
		# self.save()

		# mysub = Subscription(plan_code = self.plan.pplan_id, customer_id = self.pcus_id)
		mysub = Subscription()
		if mode:
			mysub.enable(code=self.psub_code, token=self.psub_token)
			self.active = True
			self.save()
		else:
			mysub.disable(code=self.psub_code, token=self.psub_token)
			self.active = False
			self.save()

	def disable(self):
		return self.enable(mode=False)

	def get_pdata(self):
		sub_data =	Subscription(code=self.psub_code)
		sub_data = sub_data.payload['data']
		return sub_data