import frappe
from ecommerce.services.wishlist_service import add_to_wishlist, remove_from_wishlist, get_wishlist
    

@frappe.whitelist(allow_guest=True)
def add_wishlist(user_id, item_code):
    return add_to_wishlist(user_id, item_code)

@frappe.whitelist(allow_guest=True)
def remove_wishlist(user_id, item_code):
    return remove_from_wishlist(user_id, item_code)


@frappe.whitelist(allow_guest=True)
def get_whishlist_item(user_id):
    return get_wishlist(user_id)