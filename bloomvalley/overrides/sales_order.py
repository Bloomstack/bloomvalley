import frappe

from erpnext.accounts.party import get_party_account, get_party_bank_account
from erpnext.accounts.utils import get_account_currency
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry, get_company_defaults
from frappe.utils import nowdate

def on_payment_authorized(doc, method, status=None):
    if not status:
        return

    if status in ("Completed", "Authorized"):
        doc.run_method("set_as_paid")
        frappe.db.set_value("Sales Order", doc.name, "status", "Completed")

def set_as_paid(doc, method):
    if frappe.session.user == "Guest":
        frappe.set_user("Administrator")

    #create a payment entry against the payment request
    payment_entry = create_payment_entry(doc)

def create_payment_entry(doc, submit=True):
    """Generate a payment entry against a quotation or sales order"""

    frappe.flags.ignore_account_permission = True

    gateway_accounts = frappe.get_all("Payment Gateway Account", filters={ "is_default": 1})
    if len(gateway_accounts) > 0:
        gateway_account = frappe.get_doc("Payment Gateway Account", gateway_accounts[0])
    else:
        # early bail out. We only want to deal with gateway payment entries
        return

    party_account = get_party_account("Customer", doc.get("customer"), doc.company)

    party_account_currency = doc.get("party_account_currency") or get_account_currency(party_account)

    #get payment amount from the payment request document
    bank_amount = doc.grand_total

    #If the currency of the customer matches with the currency of the quotation but not of the payment request
    if party_account_currency == doc.company_currency and party_account_currency != doc.currency:
        party_amount = doc.base_grand_total
    else:
        party_amount = doc.grand_total

    #reference document is the sales order in the payment request that was passed
    payment_entry = get_payment_entry(doc.doctype, doc.name,
        party_amount=party_amount, bank_account=gateway_account.payment_account, bank_amount=bank_amount)

    #updating details about the payment request in the payment entry
    payment_entry.update({
        "reference_no": doc.name,
        "reference_date": nowdate(),
        "remarks": "Payment Entry against {0} {1}".format(doc.doctype,
            doc.name)
    })

    if payment_entry.difference_amount:
        company_details = get_company_defaults(doc.company)

        payment_entry.append("deductions", {
            "account": company_details.exchange_gain_loss_account,
            "cost_center": company_details.cost_center,
            "amount": payment_entry.difference_amount
        })

    #submit the payment entry and return the document
    if submit:
        payment_entry.insert(ignore_permissions=True)
        payment_entry.submit()

    #creating a sales invoice once the payment entry is submitted
    si = make_sales_invoice(doc.name, ignore_permissions=True)
    si.allocate_advances_automatically = True
    si = si.insert(ignore_permissions=True)
    si.submit()
