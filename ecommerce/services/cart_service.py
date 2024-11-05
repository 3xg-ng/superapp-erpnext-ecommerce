import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Function to List Cart Items
def list_cart_items(user_id):
    try:
        query = """
            SELECT *
            FROM `tabCart`
            WHERE user_id = %s
        """
        
        items = frappe.db.sql(query, user_id, as_dict=True)

        if not items:
            raise frappe.DoesNotExistError("No items found for this user!")

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Function to Add Item to Cart
def add_to_cart(user_id, item_code):
    try:
        cart_item = frappe.db.get_value("Cart", {"user_id": user_id, "item_code": item_code}, ["quantity", "name"])

        if cart_item:
            quantity, name = cart_item
            cart_doc = frappe.get_doc("Cart", name)
            cart_doc.quantity = quantity + 1
            cart_doc.save()
        else:
            new_cart_item = frappe.get_doc({
                "doctype": "Cart",
                "user_id": user_id,
                "item_code": item_code,
                "quantity": 1
            })
            new_cart_item.insert()

        frappe.db.commit()
        return create_response(SUCCESS, f"Item {item_code} added to cart successfully!")

    except frappe.DuplicateEntryError:
        return create_response(SERVER_ERROR, "Duplicate entry found. Please try again.")
    except Exception as e:
        frappe.log_error(f"Error adding item {item_code} to cart for user {user_id}: {str(e)}", "Add to Cart Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred while adding the item: {str(e)}")


def update_cart_quantity(user_id, item_code, quantity):
    try:
        frappe.log_error(f"Starting quantity update for user {user_id} and item {item_code}.")
        cart_item = frappe.db.get_value("Cart", {"user_id": user_id, "item_code": item_code}, "quantity")

        if not cart_item:
            return create_response(NOT_FOUND, f"Item {item_code} not found in the cart.")

        if quantity == 0:
            frappe.log_error(f"Deleting item {item_code} for user {user_id}.")
            frappe.db.sql("""
                DELETE FROM `tabCart`
                WHERE user_id = %s AND item_code = %s
            """, (user_id, item_code))
            message = f"Item {item_code} removed from the cart."
        else:
            frappe.log_error(f"Updating item {item_code} to quantity {quantity} for user {user_id}.")
            frappe.db.sql("""
                UPDATE `tabCart`
                SET quantity = %s
                WHERE user_id = %s AND item_code = %s
            """, (quantity, user_id, item_code))
            message = f"Quantity of item {item_code} updated to {quantity}."

        frappe.db.commit()
        frappe.log_error(f"Quantity update successful for user {user_id} and item {item_code}.")
        return create_response(SUCCESS, message)

    except Exception as e:
        frappe.log_error(f"Error updating quantity for item {item_code} in user {user_id}'s cart: {str(e)}", "Update Cart Quantity Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred while updating the cart item: {str(e)}")



### Function to Delete Cart
def delete_cart(user_id, item_code=None):
    try:
        if item_code:
            if not frappe.db.exists("Cart", {"user_id": user_id, "item_code": item_code}):
                return create_response(NOT_FOUND, f"Item {item_code} not found in cart for user {user_id}.")
        else:
            if not frappe.db.exists("Cart", {"user_id": user_id}):
                return create_response(NOT_FOUND, f"Cart not found for user {user_id}.")

        if item_code:
            frappe.db.sql("""
                DELETE FROM `tabCart`
                WHERE user_id = %s AND item_code = %s
            """, (user_id, item_code))
            message = f"Item {item_code} deleted from cart for user {user_id}."
        else:
            frappe.db.sql("""
                DELETE FROM `tabCart`
                WHERE user_id = %s
            """, (user_id,))
            message = f"Cart for user {user_id} deleted successfully!"

        frappe.db.commit()
        return create_response(SUCCESS, message)

    except frappe.DoesNotExistError as e:
        frappe.log_error(f"Item or cart does not exist: {str(e)}", "Delete Cart Error")
        return create_response(NOT_FOUND, "Cart item or cart does not exist.")
    except Exception as e:
        frappe.log_error(f"Error deleting cart or item for user {user_id}: {str(e)}", "Delete Cart Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
