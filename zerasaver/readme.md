'''
PLAYSTACK PLANS API


Create plan
curl https://api.paystack.co/plan \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"name": "Monthly retainer", "interval": "monthly", "amount": 500000}' \
-X POST


List plan
curl "https://api.paystack.co/plan" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET


Fetch plan
curl "https://api.paystack.co/plan/PLN_gx2wn530m0i3w3m" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET


Update plan
curl "https://api.paystack.co/plan/PLN_gx2wn530m0i3w3m" \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"name": "Monthly retainer (renamed)"}' \ 
-X PUT


'''






'''
PAYSTACK CUSTOMER API

Create Customer
curl "https://api.paystack.co/customer" \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"email": "bojack@horsinaround.com"}' \ 
-X POST

List Customer
curl "https://api.paystack.co/customer" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET

Fetch Customer
curl "https://api.paystack.co/customer/1173" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET

https://api.paystack.co/customer/:id_or_customer_code
CUS_tiyf5lbhz9fc3hf


Update Customer
curl "https://api.paystack.co/customer/CUS_xnxdt6s1zg1f4nx" \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"first_name": "BoJack"}' \ 
-X PUT


Whitelist/Backlist Customer
curl https://api.paystack.co/customer/set_risk_action \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"customer": "CUS_xr58yrr2ujlft9k", "risk_action": "allow"}' \
-X POST


Deactivate Authorization
curl -X POST -H "Authorization: Bearer SECRET_KEY" -H "Content-Type: application/json" -d '{"authorization_code": "AUTH_au6hc0de"}' "https://api.paystack.co/customer/deactivate_authorization"


'''







'''
PAYSTACK TRANSACTION API

Initialize Transaction
curl https://api.paystack.co/transaction/initialize \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"reference": "7PVGX8MEk85tgeEpVDtD", "amount": 500000, "email": "customer@email.com"}' \
-X POST


Verify transaction
curl https://api.paystack.co/transaction/verify/DG4uishudoq90LD \
-H "Authorization: Bearer SECRET_KEY"


List Transaction
curl "https://api.paystack.co/transaction" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET

Fetch Transaction
curl "https://api.paystack.co/transaction/2091" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET


Charge Authorization
curl https://api.paystack.co/transaction/charge_authorization \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"authorization_code": "AUTH_72btv547", "email": "bojack@horsinaround.com", "amount": 500000}' \
-X POST


View transaction Timeline
curl https://api.paystack.co/transaction/timeline/21002R319U5139 \
-H "Authorization: Bearer SECRET_KEY"


Transaction Totals
curl "https://api.paystack.co/transaction/totals" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET


Export Transaction
curl "https://api.paystack.co/transaction/export" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET


Request Reauthorization
curl https://api.paystack.co/transaction/request_reauthorization \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"authorization_code": "AUTH_72btv547", "email": "bojack@horsinaround.com", "amount": 500000}' \
-X POST


Check Authorization
curl https://api.paystack.co/transaction/check_authorization \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"authorization_code": "AUTH_72btv547", "email": "bojack@horsinaround.com", "amount": 500000}' \
-X POST

'''







'''
PAYSTACK MISCELLANEOUS API

Fetch Settlements
url "https://api.paystack.co/settlement" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET


List Banks
curl "https://api.paystack.co/bank" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET


Resolve Card Bin
curl "https://api.paystack.co/decision/bin/539983" \
-X GET

Resolve BVN
curl "https://api.paystack.co/bank/resolve_bvn/21212917741" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET

Resolve Account Number
curl "https://api.paystack.co/bank/resolve?account_number=0022728151&bank_code=063" \
-X GET


'''






'''
PAYSTACK TRANSFER API

Initiate Transfer
curl https://api.paystack.co/transfer \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"source": "balance", "reason": "Calm down", "amount":3794800, "recipient": "RCP_gx2wn530m0i3w3m"}' \
-X POST


List Transfers
curl -X GET -H "Authorization: Bearer SECRET_KEY" "https://api.paystack.co/transfer"


Fetch Transfers
curl "https://api.paystack.co/transfer/TRF_2x5j67tnnw1t98k" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET

Finalize Tranfer
curl https://api.paystack.co/transfer/finalize_transfer \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"transfer_code": "TRF_vsyqdmlzble3uii", "otp": "928783"}' \
-X POST


Initiate Bulk Transfer
curl https://api.paystack.co/transfer \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{
	"currency": "NGN",
	"source": "balance",
	"transfers": [
	{
	"amount": 50000,
	"recipient": "RCP_db342dvqvz9qcrn"
	},
	{
	"amount": 50000,
	"recipient": "RCP_db342dvqvz9qcrn"
	}
	]
}' \
-X POST

'''






'''
PAYSTACK TRANSFER RECIPIENTS


Create Transfer Receipt
curl -X POST -H "Authorization: Bearer SECRET_KEY" -H "Content-Type: application/json" -d '{ 
   "type": "nuban",
   "name": "Zombie",
   "description": "Zombier",
   "account_number": "01000000010",
   "bank_code": "044",
   "currency": "NGN",
   "metadata": {
      "job": "Flesh Eater"
    }
 }' "https://api.paystack.co/transferrecipient"


List Tranfer Recipients
curl "https://api.paystack.co/transferrecipient" \
-H "Authorization: Bearer SECRET_KEY" 
-X GET

'''






'''
PAYSTACK TRANSFER CONTROL


Check Balance
curl -X GET -H "Authorization: Bearer SECRET_KEY" "https://api.paystack.co/balance"

Resend OTP for Transfer
curl https://api.paystack.co/transfer/resend_otp \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"transfer_code": "TRF_vsyqdmlzble3uii"}' \
-X POST


Disable  OTP Requirement for Transfer
curl https://api.paystack.co/transfer/disable_otp \
-H "Authorization: Bearer SECRET_KEY" \
-X POST


Finalize Disabling of OTP requirement for Transfers
curl https://api.paystack.co/transfer/disable_otp_finalize \
-H "Authorization: Bearer SECRET_KEY" \
-H "Content-Type: application/json" \
-d '{"otp": "928783"}' \
-X POST


Enable OTP requirement for Transfers
curl https://api.paystack.co/transfer/enable_otp \
-H "Authorization: Bearer SECRET_KEY" \
-X POST

'''






My current savings
Savings Target
Months lefts
Edit Savings Plan
Pause Saving
Quick Save
Next Scheduled Deposit Date
Next Scheduled deposit Amount
Withdrawals available
Withdraw funds
All payment log
All withdraw logs


My current savings
		All successful transactions made - withdrawals

		How much I have saved since my last withdrawal

		get customer code 
		build transaction url
		get data
		build total

		get customer code
		build transfer url
		get data
		build total


		get last withdrawal dare
		total = transaction - tranfer






Savings Target
		How much I plan to save

		get plan
		get target




Months lefts
		When my savings plan expires

		get plan
		humanize(get date end)





Edit Savings Plan
		change my savings plan

		(get_or_create_plan








Pause Saving
		pause my savings plan

		deauthorize_transactions





Quick Save
		I want to pay now so you can add it to my savings

		pay now





Next Scheduled Deposit Date
		Next time you will bill me

		get plan, get time





Next Scheduled deposit Amount
		next amount you will bill me

		get plan, get amount





* Withdrawals available
		the amount I can withdraw




Withdraw funds
		give me my money




All payment log
		all the cash i have paid

		get all transactions




All withdraw logs
		all the cash I have received

		get all transfers

Testing and verification