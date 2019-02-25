import time
from .utils import get_allplans, INTERVAL
from django.contrib.auth.models import User
from djpaystack.plan import Plan
from djpaystack.customer import Customer
from .models import ZeraPlan, USubscriptions

def create_daily_plans():
	failed = []
	for d in range(100, 5001):
		name = 'DSP-'
		name += str(d)
		desc = 'Daily Savings Plan for ' + str(d) + 'naira'
		try:
			ZeraPlan.objects.create(name= name, amount=d, frequency=1, description = desc)
		except:
			print(d, 'failed')
			failed.append(d)
			time.sleep(1)
		time.sleep(4)

	return failed


def create_zplan_from_pplan():
	er = get_allplans()
	for x in er:
		print(x['name'], x['amount'], x['id'], x['plan_code'], x['interval'])
		print(int(x['amount'] / 100))
		amount = int(x['amount'] / 100)
		name = x['name']
		try:
			z = ZeraPlan.objects.get(amount = amount)
			z.pplan_id = x['id']
			z.pplan_code = x['plan_code']
			z.name = x['name']
			z.description = x['description']
			z.frequency = INTERVAL[x['interval']]
			z.save()
		except ZeraPlan.DoesNotExist:
			print('Does not exist', x['name'], x['amount'], x['id'], x['plan_code'], x['interval'])


def create_subs():
	plans = Plan()
	all_plan = plans.list_all()
	for plan in all_plan:
		for sub in plan['subscriptions']:

			 oneplan = ZeraPlan.objects.get(pplan_code = plan['plan_code'])
			 onecus = Customer(id=sub['customer'])
			 onecus = onecus.get_data()
			 u, created = User.objects.get_or_create(email=onecus['email'])
			 USubscriptions.objects.get_or_create(user=u,
		        plan=oneplan, psub_id=sub['id'],
		        psub_code=sub['subscription_code'],
		        psub_token = sub['email_token'])
