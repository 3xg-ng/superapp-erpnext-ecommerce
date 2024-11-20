
import frappe

from ecommerce.services.order_service import list_orders, create_order, update_order, delete_order

@frappe.whitelist(allow_guest=True)
def get_orders(user_id):
   return list_orders(user_id)


@frappe.whitelist(allow_guest=True)
def create_new_order(user_id, subtotal, shipping_address, post_code, lga, discount, shipping_fee, grand_total, payment_method, status, items):
    return create_order(user_id, subtotal, shipping_address, post_code, lga, discount, shipping_fee, grand_total, payment_method, status, items)

# @frappe.whitelist(allow_guest=True)
# def create_new_order(**kwargs):
#     return kwargs


@frappe.whitelist(allow_guest=True)
def modify_order(order_id, status,  item_name, quantity):
    return update_order(order_id, status,  item_name, quantity)


@frappe.whitelist(allow_guest=True)
def remove_order(order_id):
    return delete_order(order_id)