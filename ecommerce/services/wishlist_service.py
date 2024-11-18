import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Add to wishlist
def add_to_wishlist(user_id, item_code):
    try:
        product_details = frappe.db.get_value(
            "Products", 
            {"item_code": item_code}, 
            ["product_name", "new_price", "image"], 
            as_dict=True
        )

        if not product_details:
            return create_response(NOT_FOUND, "Product not found.")

        wishlist_item = frappe.db.get_value("ProductWishlist", {"user_id": user_id, "item_code": item_code})

        
        new_wishlist_item = frappe.get_doc({
                "doctype": "ProductWishlist",
                "user_id": user_id,
                "item_code": item_code,
                "product_name": product_details["product_name"],
                "price": product_details["new_price"],
                "image": product_details["image"],
            })
        new_wishlist_item.insert()

        frappe.db.commit()
        return create_response(SUCCESS, f"Item {item_code} added to wishlist successfully!")

    except frappe.DuplicateEntryError:
        return create_response(SERVER_ERROR, "Duplicate entry found. Please try again.")
    except Exception as e:
        frappe.log_error(f"Error adding item {item_code} to wishlist for user {user_id}: {str(e)}", "Add to wishlist Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred while adding the item: {str(e)}")


def remove_from_wishlist(user_id, item_code):
    try:
        # Check if the item exists in the wishlist
        existing_entry = frappe.db.sql("""
            SELECT name FROM `tabProductWishlist`
            WHERE user_id = %s AND item_code = %s
        """, (user_id, item_code), as_dict=True)

        if not existing_entry:
            return create_response(NOT_FOUND, "Item not found in wishlist.")

        # Delete the wishlist item
        frappe.db.sql("""
            DELETE FROM `tabProductWishlist`
            WHERE user_id = %s AND item_code = %s
        """, (user_id, item_code))
        
        frappe.db.commit()

        return create_response(SUCCESS, "Item removed from wishlist successfully.")

    except Exception as e:
        frappe.log_error(message=str(e), title="Error removing from wishlist")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


def get_wishlist(user_id):
    try:
        wishlist_items = frappe.db.sql("""
            SELECT w.name, w.item_code, p.product_name, p.new_price, p.image
            FROM `tabProductWishlist`
            LEFT JOIN `tabProducts` p ON w.item_code = p.item_code
            WHERE w.user_id = %s
        """, (user_id,), as_dict=True)

        if not wishlist_items:
            return create_response(NOT_FOUND, "No items found in wishlist.")

        return create_response(SUCCESS, wishlist_items)

    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching wishlist")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
