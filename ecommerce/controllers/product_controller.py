import frappe

from ecommerce.services.product_service import list_items, list_items_category, get_item_by_code, add_new_item, update_item_by_code, delete_item_by_code, add_to_wishlist, remove_from_wishlist, get_wishlist
    
@frappe.whitelist(allow_guest=True)
def get_all_items(product_name=None, min_price=None, max_price=None, color=None, category=None, brand=None, rating=None, discount=None):
    filters = {
        "product_name": product_name,
        "min_price": min_price,
        "max_price": max_price,
        "color": color,
        "category": category,
        "brand": brand,
        "rating": rating,
        "discount": discount
    }
    return list_items(filters)


@frappe.whitelist(allow_guest=True)
def get_all_items_by_category_limit():
    return list_items_category()


@frappe.whitelist(allow_guest=True)
def get_single_item(item_code):
    return get_item_by_code(item_code)

@frappe.whitelist(allow_guest=True)
def add_item(item_code, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty):
    return add_new_item(item_code, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty)

@frappe.whitelist(allow_guest=True)
def update_item_by_code(item_code, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty):
    return update_item_by_code(item_code, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty)

@frappe.whitelist(allow_guest=True)
def delete_item(item_code):
    return delete_item_by_code(item_code)


@frappe.whitelist(allow_guest=True)
def add_wishlist(user_id, item_code):
    return add_to_wishlist(user_id, item_code)

@frappe.whitelist(allow_guest=True)
def remove_wishlist(user_id, item_code):
    return remove_from_wishlist(user_id, item_code)


@frappe.whitelist(allow_guest=True)
def get_whishlist_item(user_id):
    return get_wishlist(user_id)