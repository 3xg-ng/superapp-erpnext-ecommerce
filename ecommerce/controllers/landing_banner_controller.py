import frappe

from ecommerce.services.landing_banner_service import get_banner_a, get_banner_b, get_banner_c

@frappe.whitelist(allow_guest=True)
def list_banner_a():
    return get_banner_a() 

@frappe.whitelist(allow_guest=True)
def list_banner_b():
    return get_banner_b() 

@frappe.whitelist(allow_guest=True)
def list_banner_c():
    return get_banner_c() 
