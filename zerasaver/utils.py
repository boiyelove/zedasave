import requests
import json

# from paystackapi.paystack import Paystack

pskey = "sk_test_f49b09da906e459287b5321780593c180f0f5445"
pay_auth = 'Bearer ' + pskey
# paystack = Paystack(secret_key = pskey)
INTERVALLIST = ['hourly', 'daily', 'weekly', 'monthly', 'annually']

DAYS_OF_MONTH = (
	(1, '1st'), 
	(2,'2nd'), 
	(3,'3rd'), 
	(4,'4th'), 
	(5,'5th'), 
	(6,'6th'), 
	(7,'7th'), 
	(8,'8th'), 
	(9,'9th'), 
	(10,'10th'), 
	(11,'11th'),
	(12,'12th'), 
	(13,'13th'), 
	(14,'14th'), 
	(15,'15th'), 
	(16,'16th'), 
	(17,'17th'), 
	(18,'18th'), 
	(19,'19th'), 
	(20,'20th'), 
	(21,'21st'),
	(22,'22nd'), 
	(23,'23rd'), 
	(24,'24th'), 
	(25,'25th'), 
	(26,'26th'), 
	(27,'27th'), 
	(28,'28th'), 
	(29,'29th'), 
	(30,'30th'), 
	(31,'31st'))

DAY_OF_WEEK = (
	(1, 'Monday'),
	(2, 'Tuesday'),
	(3, 'Wednesday'),
	(4, 'Thursday'),
	(5, 'Friday'),
	(6, 'Saturday'),
	(7, 'Sunday'))


INTERVAL = {
	'daily' : 1 ,
	'weekly': 2 ,
	'monthly': 3 , 
	}

TIME_OF_DAY = {1:'4.00',
	2:'4.30',
	3:'05.00',
	4:'05.30',
	5:'06.00',
	6:'06.30',
	7:'07.00',
	8:'07.30',
	9:'08.00',
	10:'08.30',
	11:'09.00',
	12:'09.30',
	13:'10.00',
	14:'10.30',
	15:'11.00',
	16:'11.30',
	17:'12.00',
	18:'12.30',
	19:'13.00',
	20:'13.30',
	21:'14.00',
	22:'14.30',
	23:'15.00',
	24:'15.30',
	25:'16.00',
	26:'16.30',
	27:'17.00',
	28:'17.30',
	29:'18.00',
	30:'18.30',
	31:'19.00',
	32:'19.30',
	33:'20.00',
	34:'20.30',
	35:'21.00',
	36:'21:30',
	37:'22:00',
	38:'22:30',
	39:'23:00',
	40:'23:30'}

	
plan_url = 'https://api.paystack.co/plan'
header = {'Authorization': pay_auth,'Content-Type': 'application/json'}
# payload = {'name': 'DSP-400', 'description':'Daily Saving Plan 400.00', 'interval': 'daily', 'amount': '40000'}
def create_plan(payload={}):

	r = requests.post(plan_url, data=json.dumps(payload), headers=header)
	print(r.status_code)
	er = r.json()
	return [r.status_code,er['data']]

def get_allplans():
	r = requests.get(plan_url, headers=header)
	print(r.status_code)
	er = r.json()
	return er['data']

def get_plan(plan_code=''):
	if (plan_code == ''):
		raise ValueError('please provide a plan code')
	plan_url += plan_cpde
	requests.get(plan_url, headers=header)
	print(r.status_code)
	er = r.json()
	return er['data']

def update_plan(plan_id='PLN_x8nwm6ldtkb2bz2'):
	plan_url += plan_id
	payload = {'name': 'DSP-5000', 'description':'Daily Savings Plan 5000', 'amount': 500000}
	request.put(plan_url, headers=header)
	print(r.status_code)
	er = r.json()
	return er['data']

transaction_url = 'https://api.paystack.co/transaction/verify/7PVGX8MEk85tgeEpVDtD'
def verify_transaction(ref_code='', email='', plan_code = ''):
	transaction_url = 'https://api.paystack.co/transaction/verify/'
	if ref_code == '':
		raise ValueError('please provide a referece code')
	transaction_url += ref_code
	r = requests.get(transaction_url, headers=header)
	r = r.json() 
	print(r)

	if r['status']:
		data = r['data']
		cus = data['customer']
		auth = data['authorization']
		plan = data['plan']
		print(cus['email'],email,data['plan'], plan_code)
		print(type(cus['email']),type(email),type(data['plan']), type(plan_code))
		print('True0 True0')
		if ((cus['email'] == email) and (data['plan'] == plan_code)):
			print('True')
			return True
	print('False')
	return False

def create_pcustomer(email = ''):
	customer_url = "https://api.paystack.co/customer"
	payload = {'email': email}
	header = {'Authorization': pay_auth,'Content-Type': 'application/json'}
	r = requests.post(customer_url, data=json.dumps(email), headers=header)
	r = r.json()
	if r['status']:
		return [r['id'], r['customer_code']]
	return False


def current_savings(pcus_id, last_withdraw_date=''):
	transaction_url = 'https://api.paystack.co/transaction'
	if ref_code == '':
		raise ValueError('please provide a referece code')
	transaction_url += ref_code
	payload = {}
	payload['customer'] = pcus_id
	payload['status'] = 'success'
	r = requests.get(transaction_url, data=json.loads(payload), headers=header)
	r = r.json() 
	r['status']
	rdata = r['data']
	rmeta = r['meta']
	total = rmeta["total_volume"]
	totalwithdrawn = Withdrawals.objects.get_total_withdrawals(user=user)
	total = total - totalwithdrawn
	return total

# def get_date_from_week(num):
# 	from datetime import datetime, timedelta
# 	if dur == 1:
# 	targetweek =  lambda x: datetime.today() + timedelta(days = 7 * x)

# 	day = timedelta(days = x)

# 	from dateutil.relativedelta import relativedelta
# 	enddate = startdate + relativedelta(months = delta_period)

# 	six_months = timezone.now() + relativedelta(months=+6)


# 	hr = TIME_OF_DAY[1].split('.')[0]
# 	mn = TIME_OF_DAY[1].split('.')[1]
# 	thistime.replace(hour=hr, minute=mn).isoformat()


# 	user = models.OneToOneField(settings.AUTH_USER_MODEL)
# 	frequency = models.IntegerField(default=1, choices=FREQUENCY)
# 	day_of_month
# 	day_of_week
# 	deposit_amount
# 	target
# 	target_date = models.DateTimeField(null=True, blank=True)
# 	deposit_time = models.IntegerField(default=1, null=True, blank=False)

# er['amount']
# er['status']
# er['refcode']
# er['ip']


# name = 'ASP'
# desc = 'Annual'
# if form.instance.frequency == 1:
# 	name = 'DSP-'
# 	desc = 'Daily'
# elif form.instance.frequency == 2:
# 	name = 'WSP-'
# 	desc = 'Weekly'
# elif form.instance.frequency == 3:
# 	name = 'MSP-' 
# 	desc = 'Monthly'
# name += str(form.instance.deposit_amount)
# desc += ' Savings Plan for ' + str(form.instance.deposit_amount) + ' naira'

#list all transactions by customer id
hdr = {'Authorization':'Bearer sk_test_f49b09da906e459287b5321780593c180f0f5445'}
payload = {'id': '548049'}
'''
Other payloads and data types

perPage - int32 - Specify how many records you want to retrieve per page

page - int32 - Specify exactly what page you want to retrieve

customer - int32 - Specify an ID for the customer whose transactions you want to retrieve

status - string - Filter transactions by status ('failed', 'success', 'abandoned')

from - date-time - A timestamp from which to start listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
2016-09-29T00:00:05.000Z

to - date-time - A timestamp at which to stop listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
2016-09-29T00:00:05.000Z

amount - int32 - Filter transactions by amount. Specify the amount in kobo.
10000
'''


'''
transaction_url = 'https://api.paystack.co/transaction'
r = requests.get(params=payload)

{
  "status": true,
  "message": "Transactions retrieved",
  "data": [
    {
      "id": 5833,
      "domain": "test",
      "status": "failed",
      "reference": "icy9ma6jd1",
      "amount": 100,
      "message": null,
      "gateway_response": "Declined",
      "paid_at": null,
      "created_at": "2016-09-29T00:00:05.000Z",
      "channel": "card",
      "currency": "NGN",
      "ip_address": null,
      "metadata": null,
      "timeline": null,
      "customer": {
        "first_name": "Ezra",
        "last_name": "Olubi",
        "email": "ezra@cfezra.com",
        "phone": "16504173147",
        "metadata": null,
        "customer_code": "CUS_1uld4hluw0g2gn0"
      },
      "authorization": {},
      "plan": {}
    }
  ],
  "meta": {
    "total": 1,
    "skipped": 0,
    "perPage": 50,
    "page": 1,
    "pageCount": 1
  }
}
{
  "status": true,
  "message": "Transactions retrieved",
  "data": [
    {
      "id": 298126,
      "domain": "live",
      "status": "failed",
      "reference": "z1gsnks86e6kfo8",
      "amount": ,
      "message": null,
      "gateway_response": "Declined",
      "paid_at": null,
      "created_at": "2016-09-29T00:03:22.000Z",
      "channel": "card",
      "currency": "NGN",
      "ip_address": null,
      "metadata": {
                "custom_fields": [
                    {
                        "display_name": "Mobile Number",
                        "variable_name": "mobile_number",
                        "value": "+2348012345678"
                    }
                ]
        },
      "log": null,
      "fees": null,
      "paidAt": "2016-09-29T00:03:25.000Z",
      "createdAt": "2016-09-29T00:03:22.000Z",
      "authorization": {
        "authorization_code": "AUTH_86gs11dr",
        "bin": "539983",
        "last4": "0061",
        "exp_month": "08",
        "exp_year": "2018",
        "card_type": "mastercard DEBIT",
        "bank": "Guaranty Trust Bank",
        "country_code": "NG",
        "brand": "mastercard"
      },
      "customer": {
        "id": 8279,
        "first_name": "Ezra",
        "last_name": "Olubi",
        "email": "ezra@cfezra.com",
        "phone": "16504173147",
        "customer_code": "CUS_1uld4hluw0g2gn0",
        "metadata":null,
        "risk_action": "default"
      }
    }
  ],
  "meta": {
    "total": 248,
    "total_volume": 1372244,
    "skipped": 0,
    "perPage": "1",
    "page": 1,
    "pageCount": 248
  }
}


'''

