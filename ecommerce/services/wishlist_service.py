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


def remove_from_wishlist(user_id, item_code=None):
    try:
        if item_code:
            if not frappe.db.exists("ProductWishlist", {"user_id": user_id, "item_code": item_code}):
                return create_response(NOT_FOUND, f"Item {item_code} not found in wishlist for user {user_id}.")
        else:
            if not frappe.db.exists("ProductWishlist", {"user_id": user_id}):
                return create_response(NOT_FOUND, f"Wishlist not found for user {user_id}.")

        if item_code:
            frappe.db.sql("""
                DELETE FROM `tabProductWishlist`
                WHERE user_id = %s AND item_code = %s
            """, (user_id, item_code))
            message = f"Item {item_code} deleted from wishlist for user {user_id}."
        else:
            frappe.db.sql("""
                DELETE FROM `tabProductWishlist`
                WHERE user_id = %s
            """, (user_id,))
            message = f"Wishlist for user {user_id} deleted successfully!"

        frappe.db.commit()
        return create_response(SUCCESS, message)

    except frappe.DoesNotExistError as e:
        frappe.log_error(f"Item or Wishlist does not exist: {str(e)}", "Delete Wishlist Error")
        return create_response(NOT_FOUND, "Wishlist item or Wishlist does not exist.")
    except Exception as e:
        frappe.log_error(f"Error deleting Wishlist or item for user {user_id}: {str(e)}", "Delete Wishlist Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


def get_wishlist(user_id):
    try:
        query = """
            SELECT *
            FROM `tabProductWishlist`
            WHERE user_id = %s
        """
        
        items = frappe.db.sql(query, user_id, as_dict=True)

        if not items:
            return create_response(SERVER_ERROR, [])

        return create_response(SUCCESS, items)

    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

