import frappe

from ecommerce.services.product_cat_service import get_category 

@frappe.whitelist(allow_guest=True)
def list_categories():
    return get_category() 