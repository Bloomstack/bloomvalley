import frappe
import json

from frappe import _
from frappe.utils import nowdate
from frappe.integrations.utils import get_payment_gateway_controller

@frappe.whitelist(allow_guest=True)
def checkout_one(item_code, contact_info, coupon_code = "", sales_order_name=None, payment_gateway=None, currency=None, success_url="/", custom_fields="{}"):
	if isinstance(contact_info, str):
		contact_info = json.loads(contact_info)

	if isinstance(custom_fields, str):
		custom_fields = json.loads(custom_fields)

	if hasattr(contact_info, "contact_name"):
		contact_name = contact_info.get("contact_name")
	else:
		# lets find a contact
		contact_names = frappe.get_all("Contact", fields=["name"], filters={"email_id": contact_info.get("email_id")})

	# if we can't find a contact, we'll create one.
	if len(contact_names) == 0:
		contact = frappe.new_doc("Contact")
		contact.update({
			"first_name": contact_info.get("first_name"),
			"last_name": contact_info.get("last_name"),
			"email_id": contact_info.get("email_id")
		})
		contact.save(ignore_permissions=True)
		contact_name = contact.name
	else:
		contact_name = contact_names[0].name

	customer_full_name = "{} {}".format(
			contact_info.get("first_name"), contact_info.get("last_name"))
	customer_name = find_customer_by_contact(contact_name)
	if not customer_name:
		customer = frappe.new_doc("Customer")
		customer.territory = "India"
		customer.customer_group = "Individual"
		customer.customer_type = "Individual"
		customer.customer_primary_contact = contact_name
		customer.customer_name = customer_full_name
		customer.email_id = contact_info.get("email_id")
		customer.save(ignore_permissions=True)
		customer_name = customer.name

	if sales_order_name:
		so = frappe.get_doc("Sales Order", sales_order_name)
	else:
		so = frappe.new_doc("Sales Order")

	so.contact_name = contact_name
	so.delivery_date = nowdate()
	so.customer = customer_name

	if coupon_code:
		coupons = frappe.get_all("Coupon Code", filters={"coupon_code": coupon_code})

		if len(coupons) > 0:
			so.coupon_code = coupons[0].get("name")
		else:
			frappe.throw(_("Invalid Coupon Code"))

	so.update(custom_fields)

	so.append("items", {
		"item_code": item_code,
		"qty": 1
	})

	so.save(ignore_permissions=True)
	so.run_method('validate_payment')
	so.submit()

	amount = so.grand_total

	gateway_url = get_payment_gateway_url(
		so,
		payment_gateway,
		amount,
		contact_info.get("email_id"),
		customer_full_name,
		currency,
		success_url
	)

	return {
		"sales_order_name": so.name,
		"grand_total": so.grand_total,
		"contact_name": so.contact_name,
		"gateway_url": gateway_url
	}

def find_customer_by_contact(contact_name):
	customers = frappe.get_all("Customer",
		filters={
			"customer_primary_contact": contact_name
		})

	if len(customers) > 0:
		return customers[0].name

	return False

def get_payment_gateway_url(doc, payment_gateway, amount, payer_email, payer_name, currency, redirect_to):
	controller = get_payment_gateway_controller(payment_gateway)

	title = "Payment for {0} {1}".format(doc.doctype, doc.name)
	payment_details = {
		"amount": amount,
		"title": title,
		"description": title,
		"reference_doctype": doc.doctype,
		"reference_docname": doc.name,
		"payer_email": payer_email,
		"payer_name": payer_name,
		"order_id": doc.name,
		"currency": currency,
		"redirect_to": redirect_to
	}

	# Redirect the user to this url
	return controller.get_payment_url(**payment_details)
