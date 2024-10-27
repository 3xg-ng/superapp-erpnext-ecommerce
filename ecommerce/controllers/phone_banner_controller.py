import frappe

from ecommerce.services.phone_banner_service import get_samsung_banners, get_iphone_banners, get_smartphone_banners, get_tecno_banners, get_infinix_banners, get_itel_banners, get_oppo_banners 


@frappe.whitelist(allow_guest=True)
def list_smartphone_banners():
    return get_smartphone_banners() 


@frappe.whitelist(allow_guest=True)
def list_iphone_banners():
    return get_iphone_banners() 


@frappe.whitelist(allow_guest=True)
def list_samsung_banners():
    return get_samsung_banners() 


@frappe.whitelist(allow_guest=True)
def list_tecno_banners():
    return get_tecno_banners() 


@frappe.whitelist(allow_guest=True)
def list_infinix_banners():
    return get_infinix_banners() 


@frappe.whitelist(allow_guest=True)
def list_itel_banners():
    return get_itel_banners() 


@frappe.whitelist(allow_guest=True)
def list_oppo_banners():
    return get_oppo_banners() 
