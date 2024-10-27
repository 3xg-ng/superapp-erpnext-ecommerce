import frappe

from ecommerce.services.shop_banner_service import get_banners 

@frappe.whitelist(allow_guest=True)
def list_banners():
    return get_banners() 