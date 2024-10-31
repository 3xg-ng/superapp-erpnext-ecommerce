import frappe

from ecommerce.services.cart_service import list_cart_items, add_to_cart, update_cart_quantity, delete_cart

@frappe.whitelist(allow_guest=True)
def get_cart(user_id):
    return list_cart_items(user_id)

@frappe.whitelist(allow_guest=True)
def add_item_to_cart(user_id, item_code, product_name, image, seller_name, quantity):
    return add_to_cart(user_id, item_code, product_name, image, seller_name, quantity)

@frappe.whitelist(allow_guest=True)
def update_cart_item(user_id, item_code, product_name, image, seller_name, quantity):
    return update_cart_quantity(user_id, item_code, product_name, image, seller_name, quantity)

@frappe.whitelist(allow_guest=True)
def clear_cart(user_id):
    return delete_cart(user_id)