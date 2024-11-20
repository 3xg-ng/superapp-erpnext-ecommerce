
import frappe

from ecommerce.services.order_service import list_orders, create_order, update_order, delete_order

@frappe.whitelist(allow_guest=True)
def get_orders(user_id):
   return list_orders(user_id)


@frappe.whitelist(allow_guest=True)
def create_new_order(shipping_address, lga, post_code, subtotal, items, discount, shipping_fee, grand_total, payment_method, user_id, status):
    return create_order(shipping_address, lga, post_code, subtotal, items, discount, shipping_fee, grand_total, payment_method, user_id, status)


@frappe.whitelist(allow_guest=True)
def modify_order(order_id, status,  item_name, quantity):
    return update_order(order_id, status,  item_name, quantity)


@frappe.whitelist(allow_guest=True)
def remove_order(order_id):
    return delete_order(order_id)