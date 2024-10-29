import frappe

from ecommerce.services.product_service import list_items, list_items_category, list_items_smartphone, list_items_accessories, list_items_laptops, list_items_home_appliance, list_items_kiddies, list_items_new_arrival, list_items_best_seller, list_items_official_store, get_product_by_id, add_new_item, update_item_by_code, delete_item_by_code
    
@frappe.whitelist(allow_guest=True)
def get_all_items():
    # Get parameters from request
    color = frappe.form_dict.get("color")
    product_name = frappe.form_dict.get("product_name")
    min_price = frappe.form_dict.get("min_price")
    max_price = frappe.form_dict.get("max_price")
    brand = frappe.form_dict.get("brand")
    model = frappe.form_dict.get("model")
    sort_by = frappe.form_dict.get("sort_by")
    sort_order = frappe.form_dict.get("sort_order", "ASC")  # Default to ascending order if not specified
    
    # Convert min_price and max_price to float if they are provided
    if min_price:
        min_price = float(min_price)
    if max_price:
        max_price = float(max_price)
    
    # Call the list_items function with the retrieved parameters
    return list_items(
        color=color,
        product_name=product_name,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        model=model,
        sort_by=sort_by,
        sort_order=sort_order
    )



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
def get_single_item(product_id):
    return get_product_by_id(product_id)

@frappe.whitelist(allow_guest=True)
def add_item(product_id, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty):
    return add_new_item(product_id, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty)

@frappe.whitelist(allow_guest=True)
def update_item_by_code(product_id, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty):
    return update_item_by_code(product_id, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty)

@frappe.whitelist(allow_guest=True)
def delete_item(product_id):
    return delete_item_by_code(product_id)
