import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response
from datetime import datetime

### Function to List All Orders for a User
def list_orders(user_id):
    try:
        orders_query = """
            SELECT *
            FROM `tabOrder`
            WHERE user_id = %s
        """
        orders = frappe.db.sql(orders_query, user_id, as_dict=True)

        if not orders:
            raise frappe.DoesNotExistError("No orders found for this user!")

        cart_query = """
            SELECT item_code, quantity, price, seller_name
            FROM `tabCart`
            WHERE user_id = %s
        """
        cart_items = frappe.db.sql(cart_query, user_id, as_dict=True)

        for order in orders:
            order["item"] = cart_items

        return create_response(SUCCESS, orders)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching orders and cart items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

    

def create_order(data):
    try:
        required_orders_keys = ["shipping_address", "lga", "post_code", "subtotal", "items", "discount", "shipping_fee", "grand_total", "payment_method", "user_id", "status"]
        required_keys = ["item_code", "price", "quantity", "seller_name"]
        
        # Check if all required order keys are present in data
        if not all(key in data for key in required_orders_keys):
            raise ValueError("Missing required order data")
        
        # Extract items from data
        items = data.get("items")
        
        # Ensure items is a list of dictionaries
        if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
            raise ValueError("Items must be a list of dictionaries.")

        validated_items = []
        # Validate each item
        for item in items:
            if not all(key in item for key in required_keys):
                raise ValueError("Each item must include item_code, price, quantity, and seller_name.")
            validated_items.append({
                "doctype": "Order Item",
                "item_code": item["item_code"],
                "price": item["price"],
                "quantity": item["quantity"],
                "seller_name": item["seller_name"]
            })

        # Create the sales order document
        sales_order = frappe.get_doc({
            "doctype": "Order",
            "shipping_address": data["shipping_address"],
            "lga": data["lga"],
            "post_code": data["post_code"],
            "net_total": data["subtotal"],
            "discount": data["discount"],
            "shipping_fee": data["shipping_fee"],
            "grand_total": data["grand_total"],
            "payment_method": data["payment_method"],
            "user_id": data["user_id"],
            "status": "Drafted",
            "items": validated_items
        })
        
        # Insert and commit the sales order
        sales_order.insert()
        frappe.db.commit()

        # Return the order ID
        order_id = sales_order.name
        return create_response(SUCCESS, {"order_id": order_id})

    except ValueError as e:
        # Log validation error
        frappe.log_error(f"Data validation error for user {data['user_id']}: {str(e)}", "Order Creation Validation Error")
        return create_response(BAD_REQUEST, f"Validation error: {str(e)}")

    except frappe.ValidationError as e:
        # Log Frappe validation error
        frappe.log_error(f"Frappe validation error for user {data['user_id']}: {str(e)}", "Order Creation Validation Error")
        return create_response(BAD_REQUEST, f"Frappe validation error: {str(e)}")

    except Exception as e:
        # Log unexpected errors
        frappe.log_error(f"Error creating order for user {data['user_id']}: {str(e)}", "Order Creation Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def update_order(order_id, status=None, items=None):
    
    try:
        order = frappe.get_doc("Sales Order", order_id)

        if status:
            order.status = status

        if items:
            order.items = [] 
            for item in items:
                order.append("items", {
                    "item_code": item["item_code"],
                    "item_name": item["item_name"],
                    "qty": item["qty"],
                    "rate": item["rate"],
                    "amount": item["amount"]
                })

        order.save()
        frappe.db.commit()

        return create_response(SUCCESS, f"Order {order_id} updated successfully!")

    except frappe.DoesNotExistError:
        return create_response(NOT_FOUND, f"Order {order_id} not found!")

    except Exception as e:
        frappe.log_error(f"Error updating order {order_id}: {str(e)}", "Update Order Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


def delete_order(order_id):
    """
    Delete an existing order by its ID.

    :param order_id: The ID of the order to be deleted.
    :return: JSON response indicating success or error.
    """
    try:
        order = frappe.get_doc("Sales Order", order_id)
        order.delete()
        frappe.db.commit()

        return create_response(SUCCESS, f"Order {order_id} deleted successfully!")

    except frappe.DoesNotExistError:
        return create_response(NOT_FOUND, f"Order {order_id} not found!")

    except Exception as e:
        frappe.log_error(f"Error deleting order {order_id}: {str(e)}", "Delete Order Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
