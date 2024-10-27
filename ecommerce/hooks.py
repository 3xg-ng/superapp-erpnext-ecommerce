app_name = "ecommerce"
app_title = "Ecommerce"
app_publisher = "3XG"
app_description = "e-Commerce app for 3xg.africa"
app_email = "Products3xg@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ecommerce/css/ecommerce.css"
# app_include_js = "/assets/ecommerce/js/ecommerce.js"

# include js, css files in header of web template
# web_include_css = "/assets/ecommerce/css/ecommerce.css"
# web_include_js = "/assets/ecommerce/js/ecommerce.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ecommerce/public/scss/website"

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
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ecommerce.utils.jinja_methods",
# 	"filters": "ecommerce.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ecommerce.install.before_install"
# after_install = "ecommerce.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ecommerce.uninstall.before_uninstall"
# after_uninstall = "ecommerce.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ecommerce.utils.before_app_install"
# after_app_install = "ecommerce.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ecommerce.utils.before_app_uninstall"
# after_app_uninstall = "ecommerce.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ecommerce.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ecommerce.tasks.all"
# 	],
# 	"daily": [
# 		"ecommerce.tasks.daily"
# 	],
# 	"hourly": [
# 		"ecommerce.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ecommerce.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ecommerce.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ecommerce.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ecommerce.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ecommerce.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ecommerce.utils.before_request"]
# after_request = ["ecommerce.utils.after_request"]

# Job Events
# ----------
# before_job = ["ecommerce.utils.before_job"]
# after_job = ["ecommerce.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ecommerce.auth.validate"
# ]

# hooks.py

app_include_api = [
    
    # Product API Endpoints
    {
        "method": "GET",
        "path": "/api/method/get_all_items",
        "handler": "ecommerce.controllers.product_controller.get_all_items"
    },
    {
        "method": "POST",
        "path": "/api/method/add_item",
        "handler": "ecommerce.controllers.product_controller.add_item"
    },
    {
        "method": "PUT",
        "path": "/api/method/update_item",
        "handler": "ecommerce.controllers.product_controller.update_item"
    },
    {
        "method": "DELETE",
        "path": "/api/method/delete_item/<string:item_code>",
        "handler": "ecommerce.controllers.product_controller.delete_item"
    },
    
    
    # Cart API Endpoints
    {
        "method": "GET",
        "path": "/api/method/get_cart",
        "handler": "ecommerce.controllers.cart_controller.get_cart"
    },
    {
        "method": "POST",
        "path": "/api/method/add_item_to_cart",
        "handler": "ecommerce.controllers.cart_controller.add_item_to_cart"
    },
    {
        "method": "PUT",
        "path": "/api/method/clear_cart",
        "handler": "ecommerce.controllers.cart_controller.clear_cart"
    },
    {
        "method": "DELETE",
        "path": "/api/method/delete_item/<string:item_code>",
        "handler": "ecommerce.controllers.cart_controller.delete_item"
    },
    
    
    # Order API Endpoints
    {
        "method": "GET",
        "path": "/api/method/ecommerce.controllers.order_controller.get_orders",
        "handler": "ecommerce.controllers.order_controller.get_orders"
    },
    {
        "method": "POST",
        "path": "/api/method/ecommerce.controllers.order_controller.create_new_order",
        "handler": "ecommerce.controllers.order_controller.create_new_order"
    },
    {
        "method": "PUT",
        "path": "/api/method/ecommerce.controllers.order_controller.modify_order",
        "handler": "ecommerce.controllers.order_controller.modify_order"
    },
    {
        "method": "DELETE",
        "path": "/api/method/ecommerce.controllers.order_controller.remove_order",
        "handler": "ecommerce.controllers.order_controller.remove_order"
    },
    
]
