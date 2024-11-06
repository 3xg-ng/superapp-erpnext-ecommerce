import json
import frappe

from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response
from ecommerce.services.order_service import list_orders, create_order, update_order, delete_order

@frappe.whitelist(allow_guest=False)
def get_orders(user_id):
   return list_orders(user_id)


@frappe.whitelist(allow_guest=False)
def create_new_order(shipping_address, post_code, subtotal, shipping_fee, discount, total, payment_method, user_id, status):
    return create_order(shipping_address, post_code, subtotal, shipping_fee, discount, total, payment_method, user_id, status)


@frappe.whitelist(allow_guest=False)
def modify_order(order_id, status,  item_name, quantity):
    return update_order(order_id, status,  item_name, quantity)


@frappe.whitelist(allow_guest=False)
def remove_order(order_id):
    return delete_order(order_id)