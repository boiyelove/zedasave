My current savings
def get_transactionlist(customer_id = '', from_date=''):
  return dict_obj

def my_current_savings(user):
  get customer user_id
  get the date of last withdrawal
  get successful transactions with the above data
  sum up these amounts
  return the sum

def my_savings_target(user):
  get current user plan
  get target
  return target

def months_left(user):
  get current plan
  get time to end
  return time_left

def create_savings_plan(user_data):
  get form data
  check plan by amount and interval and currency
  if it exists
  get plan id from object
  create subscriber on that plan



  if it doesn't exist
  create plan foreign
  create plan locally with plan_id from foreign
  
  Data sent
  curl https://api.paystack.co/plan \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"name": "Monthly retainer", "interval": "monthly", "amount": 500000}' \
-X POST

  Data received
  {
  "status": true,
  "message": "Plan created",
  "data": {
    "name": "Monthly retainer",
    "amount": 500000,
    "interval": "monthly",
    "integration": 100032,
    "domain": "test",
    "plan_code": "PLN_gx2wn530m0i3w3m",
    "send_invoices": true,
    "send_sms": true,
    "hosted_page": false,
    "currency": "NGN",
    "id": 28,
    "createdAt": "2016-03-29T22:42:50.811Z",
    "updatedAt": "2016-03-29T22:42:50.811Z"
    }
  }


  create subscription of the plan
  data sent
  curl https://api.paystack.co/subscription \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"customer": "CUS_xnxdt6s1zg1f4nx", "plan": "PLN_gx2wn530m0i3w3m"}' \
-X POST

  data received
  {
  "status": true,
  "message": "Subscription successfully created",
  "data": {
    "customer": 1173,
    "plan": 28,
    "integration": 100032,
    "domain": "test",
    "start": 1459296064,
    "status": "active",
    "quantity": 1,
    "amount": 50000,
    "authorization": 79,
    "subscription_code": "SUB_vsyqdmlzble3uii",
    "email_token": "d7gofp6yppn3qz7",
    "id": 9,
    "createdAt": "2016-03-30T00:01:04.687Z",
    "updatedAt": "2016-03-30T00:01:04.687Z"
  }
  }
  legend
  customer string REQUIRED (Customer email address or customer code)
  plan string REQUIRED Plan_code


  authorization string If customer has multiple authorizations, you can set the desired authorization you wish to use for this subscription here. If this is not supplied, the customer's most recent authorization would be used

  start_date string Set the date for the first debit. (ISO 8601 format) 2017-05-16T00:30:13+01:00

  Note the email_token attribute for the subscription object. We create one on each subscription so customers can cancel their subscriptions from within the invoices sent to their mailboxes. Since they are not authorized, the email tokens are what we use to authenticate the requests over the API.

  
