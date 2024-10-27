import frappe

from ecommerce.services.product_service import list_items, list_items_category, list_items_smartphone, list_items_accessories, list_items_laptops, list_items_home_appliance, list_items_kiddies, list_items_new_arrival, list_items_best_seller, list_items_official_store, get_item_by_code, add_new_item, update_item_by_code, delete_item_by_code
    
@frappe.whitelist(allow_guest=True)
def get_all_items():
    return list_items()


@frappe.whitelist(allow_guest=True)
def get_all_items_by_category_limit():
    return list_items_category()


# Smartphones
@frappe.whitelist(allow_guest=True)
def get_all_items_by_smartphone():
    return list_items_smartphone()

# Accessories
@frappe.whitelist(allow_guest=True)
def get_all_items_by_accessories():
    return list_items_accessories()

# Laptops
@frappe.whitelist(allow_guest=True)
def get_all_items_by_laptops():
    return list_items_laptops()

# Home appliances
@frappe.whitelist(allow_guest=True)
def get_all_items_by_home_appliance():
    return list_items_home_appliance()

# Kiddies
@frappe.whitelist(allow_guest=True)
def get_all_items_by_kiddies():
    return list_items_kiddies()

# New Arrival
@frappe.whitelist(allow_guest=True)
def get_all_items_by_new_arrival():
    return list_items_new_arrival()

# Best Seller
@frappe.whitelist(allow_guest=True)
def get_all_items_by_best_seller():
    return list_items_best_seller()

# Official Store
@frappe.whitelist(allow_guest=True)
def get_all_items_by_official_store():
    return list_items_official_store()

@frappe.whitelist(allow_guest=True)
def get_single_item(item_code):
    return get_item_by_code(item_code)

@frappe.whitelist(allow_guest=True)
def add_item(sku, product_name, category, old_price, new_price, image, rating, brand, description, product_line, model, weight, availability, color, quantity, warranty):
    return add_new_item(sku, product_name, category, old_price, new_price, image, rating, brand, description, product_line, model, weight, availability, color, quantity, warranty)

@frappe.whitelist(allow_guest=True)
def update_item_by_code(sku, product_name, category, old_price, new_price, image, rating, brand, description, product_line, model, weight, availability, color, quantity, warranty, collection):
    return update_item_by_code(sku, product_name, category, old_price, new_price, image, rating, brand, description, product_line, model, weight, availability, color, quantity, warranty, collection)

@frappe.whitelist(allow_guest=True)
def delete_item(item_code):
    return delete_item_by_code(item_code)
