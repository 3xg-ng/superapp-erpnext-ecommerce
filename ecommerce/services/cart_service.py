import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Function to List Cart Items
def list_cart_items(user_id):
    
    try:
        cart_items = frappe.db.sql("""
            SELECT product_id, product_name, quantity
            FROM `tabCart`
            WHERE user_id = %s
        """, (user_id,), as_dict=True)

        if not cart_items:
            return create_response(NOT_FOUND, "Cart is empty!")

        return create_response(SUCCESS, cart_items)

    except Exception as e:
        frappe.log_error(f"Error listing cart items for user {user_id}: {str(e)}", "Cart Listing Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred while fetching cart items: {str(e)}")

### Function to Add Item to Cart
def add_to_cart(user_id, product_id, product_name, quantity=1):
    
    try:
        # Check if the item already exists in the user's cart
        cart_item = frappe.db.get_value("Cart", {"user_id": user_id, "product_id": product_id}, "quantity")

        if cart_item:
            # Update the quantity of the existing item
            frappe.db.sql("""
                UPDATE `tabCart`
                SET quantity = quantity + %s
                WHERE user_id = %s AND product_id = %s
            """, (quantity, user_id, product_id))
        else:
            # Insert a new item into the cart
            new_cart_item = frappe.get_doc({
                "doctype": "Cart",
                "user_id": user_id,
                "item_code": product_id,
                "product_name": product_name,
                "quantity": quantity
            })
            new_cart_item.insert()

        frappe.db.commit()
        return create_response(SUCCESS, f"Item {product_id} added to cart successfully!")

    except frappe.DuplicateEntryError:
        return create_response(SERVER_ERROR, "Duplicate entry found. Please try again.")
    except Exception as e:
        frappe.log_error(f"Error adding item {product_id} to cart for user {user_id}: {str(e)}", "Add to Cart Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred while adding the item: {str(e)}")


def update_cart_quantity(user_id, product_id, quantity):
    
    try:
        cart_item = frappe.db.get_value("Cart", {"user_id": user_id, "product_id": product_id}, "quantity")

        if not cart_item:
            return create_response(NOT_FOUND, f"Item {product_id} not found in the cart.")

        if quantity == 0:
            frappe.db.sql("""
                DELETE FROM `tabCart`
                WHERE user_id = %s AND product_id = %s
            """, (user_id, product_id))
            message = f"Item {product_id} removed from the cart."
        else:
            # Update the item quantity in the cart
            frappe.db.sql("""
                UPDATE `tabCart`
                SET quantity = %s
                WHERE user_id = %s AND product_id = %s
            """, (quantity, user_id, product_id))
            message = f"Quantity of item {product_id} updated to {quantity}."

        frappe.db.commit()
        return create_response(SUCCESS, message)

    except Exception as e:
        frappe.log_error(f"Error updating cart item {product_id} for user {user_id}: {str(e)}", "Update Cart Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred while updating the cart item: {str(e)}")

### Function to Delete Cart
def delete_cart(user_id):
    
    try:
        if not frappe.db.exists("Cart", {"user_id": user_id}):
            return create_response(NOT_FOUND, "Cart not found!")

        # Delete the user's cart
        frappe.db.sql("""
            DELETE FROM `tabCart`
            WHERE user_id = %s
        """, (user_id,))

        frappe.db.commit()
        return create_response(SUCCESS, f"Cart for user {user_id} deleted successfully!")

    except Exception as e:
        frappe.log_error(f"Error deleting cart for user {user_id}: {str(e)}", "Delete Cart Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred while deleting the cart: {str(e)}")
