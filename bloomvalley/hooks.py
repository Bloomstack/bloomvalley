# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "bloomvalley"
app_title = "Bloom Valley"
app_publisher = "Neil Lasrado"
app_description = "Website for Bloom Valley"
app_icon = "octicon octicon-file-directory"
app_color = "green"
app_email = "neil@bloomstack.com"
app_license = "GPL v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bloomvalley/css/bloomvalley.css"
# app_include_js = "/assets/bloomvalley/js/bloomvalley.js"

# include js, css files in header of web template
web_include_css = "/assets/css/bloomvalley.css"
web_include_js = "/assets/js/bloomvalley.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "bloomvalley.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "bloomvalley.install.before_install"
# after_install = "bloomvalley.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bloomvalley.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
    "Sales Order": {
        "on_payment_authorized": "bloomvalley.overrides.sales_order.on_payment_authorized",
        "set_as_paid": "bloomvalley.overrides.sales_order.set_as_paid"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"bloomvalley.tasks.all"
# 	],
# 	"daily": [
# 		"bloomvalley.tasks.daily"
# 	],
# 	"hourly": [
# 		"bloomvalley.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bloomvalley.tasks.weekly"
# 	]
# 	"monthly": [
# 		"bloomvalley.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "bloomvalley.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "bloomvalley.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "bloomvalley.task.get_dashboard_data"
# }

# Exempt doctype for cancel
# -----------------------
#
# auto_cancel_exempt_doctypes = ["Auto Repeat"]

