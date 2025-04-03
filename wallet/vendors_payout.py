
from django.conf import settings
import requests
class RazorpayVendorsPayouts():
    def __init__(self):
        self.auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        self.base_url = "https://api.razorpay.com/v1"

    def create_vendor(self,data):
        vendor_data = {
            "name": "Vendor Name",
            "email": "vendor@example.com",
            "contact": data["contact_number"],
            "type": "vendor"
        }

        response = requests.post(f"{self.base_url}/contacts", auth=self.auth, json=vendor_data)
        result = response.json()
        print("Vendor Created:", result)
        return result
        # vendor = {
        #     "id": "cont_ABC123456", #this is the Contact ID for the vendor.
        #     "name": "Vendor Name",
        #     "contact": "9876543210",
        #     "email": "vendor@example.com",
        #     "type": "vendor"
        # }

    def create_vendors_fund_account(self,data):
        """Create Fund Account for Vendor"""
        fund_account_data = {
            "contact_id": data["contact_id"],  # This comes from create_vendor() id
            "account_type": "bank_account",
            "bank_account": {
                "name": data["bank_account_holder_name"],
                "ifsc": data["bank_ifsc_code"],
                "account_number": data["bank_account_number"]
            }
        }

        response = requests.post(f"{self.base_url}/fund_accounts", auth=self.auth, json=fund_account_data)
        result = response.json()
        print("Fund Account Created:", result)
        return result
        #{
        #     "id": "fa_DEF789012", #this is the Fund Account ID for payouts.
        #     "contact_id": "cont_ABC123456",
        #     "account_type": "bank_account"
        # }

    def fund_transfer_to_vendor(self,data):
        """Transfer funds to Vendor"""
        payout_data = {
            "account_number": "2323230054343434",  # Your RazorpayX Account Number
            "fund_account_id": data["fund_account_id"],  # This comes from create_vendors_fund_account()
            "amount": data["amount"],  # Amount in paise (₹5000 = 500000)
            "currency": "INR",
            "mode": "IMPS",
            "purpose": "vendor_payment",
            "queue_if_low_balance": True,
            "reference_id": data["reference_id"],
            "narration": "Vendor Payment"
        }

        response = requests.post(f"{self.base_url}/payouts", auth=self.auth, json=payout_data)
        result = response.json()
        print("Payout Created:", result)
        return result  # Returns the Payout details
