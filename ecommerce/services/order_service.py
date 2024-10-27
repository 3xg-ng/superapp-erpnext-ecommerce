import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response
from datetime import datetime

### Function to List All Orders for a User
def list_orders(user_id):
    try:
        orders = frappe.db.sql("""
            SELECT name AS order_id, total_price, status
            FROM `tabSales Order`
            WHERE user_id = %s
            ORDER BY creation DESC;
        """, (user_id,), as_dict=True)

        if not orders:
            raise frappe.DoesNotExistError("No orders found for this user!")

        for order in orders:
            order_items = frappe.db.sql("""
                SELECT item_code, item_name, qty, rate, amount
                FROM `tabSales Order Item`
                WHERE parent = %s
            """, (order["order_id"],), as_dict=True)
            order["items"] = order_items

        return create_response(SUCCESS, orders)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))

    except Exception as e:
        frappe.log_error(f"Error fetching orders for user {user_id}: {str(e)}", "Order Listing Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

### Function to Create a New Order
def create_order(user_id, items, total_price, status="Draft"):
    
    try:
        # Create a new Sales Order document
        new_order = frappe.get_doc({
            "doctype": "Sales Order",
            "user_id": user_id,
            "total_price": total_price,
            "status": status
        })
        
        # Add items to the order
        for item in items:
            new_order.append("items", {
                "item_code": item["item_code"],
                "item_name": item["item_name"],
                "qty": item["qty"],
                "rate": item["rate"],
                "amount": item["amount"]
            })
        
        new_order.insert()
        frappe.db.commit()

        return create_response(SUCCESS, f"Order {new_order.name} created successfully!")

    except Exception as e:
        frappe.log_error(f"Error creating order for user {user_id}: {str(e)}", "Create Order Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


### Function to Update an Existing Order
def update_order(order_id, status=None, items=None):
    
    try:
        # Fetch the existing order
        order = frappe.get_doc("Sales Order", order_id)

        # Update status if provided
        if status:
            order.status = status

        # Update items if provided
        if items:
            order.items = []  # Clear existing items
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


### Function to Delete an Order
def delete_order(order_id):
    """
    Delete an existing order by its ID.

    :param order_id: The ID of the order to be deleted.
    :return: JSON response indicating success or error.
    """
    try:
        # Fetch and delete the order
        order = frappe.get_doc("Sales Order", order_id)
        order.delete()
        frappe.db.commit()

        return create_response(SUCCESS, f"Order {order_id} deleted successfully!")

    except frappe.DoesNotExistError:
        return create_response(NOT_FOUND, f"Order {order_id} not found!")

    except Exception as e:
        frappe.log_error(f"Error deleting order {order_id}: {str(e)}", "Delete Order Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
