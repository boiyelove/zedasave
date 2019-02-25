import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from accounts.models import UserProfile
from djpaystack.customer import Customer
from .models import ZeraPlan, UserSavingsPlan
from .utils import create_plan, INTERVALLIST, create_pcustomer


@receiver(post_save, sender=ZeraPlan)
def create_paystack_plan(instance, created, sender, **kwargs):
	if created and (not instance.pplan_id and not instance.pplan_code):
		payload = {}
		payload['amount'] = instance.amount * 100
		payload['interval'] = INTERVALLIST[instance.frequency]
		payload['name'] =  instance.name
		payload['desciption'] = instance.description
		r = create_plan(payload)
		if (r[0] > 200) and (r[0] < 300):
			er = r[1]
			instance.pplan_id = er['plan_id']
			instance.pplan_code = er['plan_code']
			instance.save()
			print(instance.name, 'created and saved with', plan_id)

@receiver(post_save, sender=UserProfile)
def update_userplan_customer(instance, created, sender, **kwargs):
	if created:
		cc = Customer()
		cc.create(instance.user.email,
			firstname = instance.user.first_name,
			lastname = instance.user.last_name,
			phone = instance.phone)
		print('cc before', cc)
		cc = cc.get_data()
		cc = cc['data']
		print('cc after is',cc)
		if cc:
			uplan = UserSavingsPlan.objects.create(user = instance.user,
			pcus_id = cc['id'],
			pcus_code = cc['customer_code'])
		else:
			uplan = UserSavingsPlan.objects.create(user = instance.user)

# @receiver(pre_save, sender=UserSavingsPlan)
# def update_userSavingsPlan(instance, sender, **kwargs):
# 	if instance.target:
# 		if instance.frequency == 	1:
# 			target_date = timezone.now() + datetime.timedelta(days = instance.target)
# 		elif instance.frequency == 2:
# 			target_date = timezone.now() + datetime.timedelta(weeks = instance.target)
# 		elif instance.frequency == 3:
# 			target_date = timezone.now() + datetime.timedelta(instance.target *365/12)
# 		instance.target_date = target_date