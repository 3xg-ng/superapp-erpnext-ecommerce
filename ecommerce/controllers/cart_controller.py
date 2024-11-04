import frappe

from ecommerce.services.cart_service import list_cart_items, add_to_cart, update_cart_quantity, delete_cart

@frappe.whitelist(allow_guest=True)
def get_cart():
    return list_cart_items()

@frappe.whitelist(allow_guest=True)
def add_item_to_cart(user_id, item_code):
    return add_to_cart(user_id, item_code)

@frappe.whitelist(allow_guest=True)
def update_cart_item(user_id, item_code, quantity):
    return update_cart_quantity(user_id, item_code, quantity)

@frappe.whitelist(allow_guest=True)
def clear_cart(user_id, item_code):
    return delete_cart(user_id, item_code)