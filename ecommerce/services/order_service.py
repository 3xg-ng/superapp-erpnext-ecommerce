import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response

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
            raise create_response(SERVER_ERROR, [])

        cart_query = """
            SELECT item_code, quantity, price, seller_name
            FROM `tabOrder Item`
            WHERE user_id = %s
        """
        cart_items = frappe.db.sql(cart_query, user_id, as_dict=True)

        for cart in cart_items:
            cart["item"] = cart_items

        return create_response(SUCCESS, orders)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching orders and cart items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

    

def create_order(order_id, user_id, subtotal, shipping_address, post_code, lga, discount, shipping_fee, grand_total, payment_method, status, items):
    try:
        required_keys = ["item_code", "price", "quantity", "seller_name"]
        
        if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
            raise ValueError("Items must be a list of dictionaries.")

        validated_items = []
        
        for item in items:
            if not all(key in item for key in required_keys):
                raise ValueError("Each item must include item_code, price, quantity, and seller_name.")
            validated_items.append({
                "doctype": "Order Item",
                "item_code": item["item_code"],
                "price": item["price"],
                "quantity": item["quantity"],
                "seller_name": item["seller_name"],
                "user_id": item["user_id"]
            })

        sales_order = frappe.get_doc({
            "doctype": "Order",
            "shipping_address": shipping_address,
            "lga": lga,
            "post_code": post_code,
            "net_total": subtotal,
            "discount": discount,
            "shipping_fee": shipping_fee,
            "grand_total": grand_total,
            "payment_method": payment_method,
            "order_id": order_id,
            "user_id": user_id,
            "status": status,
            "items": validated_items
        })
        
        sales_order.insert(ignore_permissions=True)
        frappe.db.commit()

        order_id = sales_order.name
        return create_response(SUCCESS, {"order_id": order_id})

    except ValueError as e:
        frappe.log_error(f"Data validation error for user {user_id}: {str(e)}", "Order Creation Validation Error")
        return create_response(BAD_REQUEST, f"Validation error: {str(e)}")

    except frappe.ValidationError as e:
        frappe.log_error(f"Frappe validation error for user {user_id}: {str(e)}", "Order Creation Validation Error")
        return create_response(BAD_REQUEST, f"Frappe validation error: {str(e)}")

    except Exception as e:
        frappe.log_error(f"Error creating order for user {user_id}: {str(e)}", "Order Creation Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")


def update_order(order_id, user_id, subtotal=None, shipping_address=None, post_code=None, lga=None, discount=None, shipping_fee=None, grand_total=None, payment_method=None, status=None, items=None):
    try:
        sales_order = frappe.get_doc("Order", order_id)
        
        if not sales_order:
            raise ValueError(f"Order with ID {order_id} does not exist.")

        if user_id and sales_order.user_id != user_id:
            raise ValueError("User ID does not match the owner of the order.")
        
        if subtotal is not None:
            sales_order.net_total = subtotal
        if shipping_address is not None:
            sales_order.shipping_address = shipping_address
        if post_code is not None:
            sales_order.post_code = post_code
        if lga is not None:
            sales_order.lga = lga
        if discount is not None:
            sales_order.discount = discount
        if shipping_fee is not None:
            sales_order.shipping_fee = shipping_fee
        if grand_total is not None:
            sales_order.grand_total = grand_total
        if payment_method is not None:
            sales_order.payment_method = payment_method
        if status is not None:
            sales_order.status = status

        if items is not None:
            required_keys = ["item_code", "price", "quantity", "seller_name"]
            
            if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
                raise ValueError("Items must be a list of dictionaries.")
            
            validated_items = []
            for item in items:
                if not all(key in item for key in required_keys):
                    raise ValueError("Each item must include item_code, price, quantity, and seller_name.")
                validated_items.append({
                    "doctype": "Order Item",
                    "item_code": item["item_code"],
                    "price": item["price"],
                    "quantity": item["quantity"],
                    "seller_name": item["seller_name"],
                    "user_id": item.get("user_id", sales_order.user_id),
                })
            
            sales_order.items = validated_items

        sales_order.save()
        frappe.db.commit()

        return create_response(SUCCESS, {"order_id": sales_order.name, "message": "Order updated successfully."})

    except ValueError as e:
        frappe.log_error(f"Data validation error for user {user_id}: {str(e)}", "Order Update Validation Error")
        return create_response(BAD_REQUEST, f"Validation error: {str(e)}")

    except frappe.ValidationError as e:
        frappe.log_error(f"Frappe validation error for user {user_id}: {str(e)}", "Order Update Validation Error")
        return create_response(BAD_REQUEST, f"Frappe validation error: {str(e)}")

    except Exception as e:
        frappe.log_error(f"Error updating order for user {user_id}: {str(e)}", "Order Update Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def delete_order(user_id, order_id):
    try:
        if order_id:
            if not frappe.db.exists("Order", {"user_id": user_id, "name": order_id}):
                return create_response(NOT_FOUND, f"{order_id} not found in order for user {user_id}.")
        else:
            if not frappe.db.exists("Order", {"user_id": user_id}):
                return create_response(NOT_FOUND, f"Order not found for user {user_id}.")

        if order_id:
            frappe.db.sql("""
                DELETE FROM `tabOrder`
                WHERE user_id = %s AND name = %s
            """, (user_id, order_id))
            # message = f"Item {order_id} deleted from order for user {user_id}."
            message = f"{order_id} order has been deleted successfully."
        else:
            frappe.db.sql("""
                DELETE FROM `tabOrder`
                WHERE user_id = %s
            """, (user_id,))
            message = f"Order for user {user_id} deleted successfully!"

        frappe.db.commit()
        return create_response(SUCCESS, message)

    except frappe.DoesNotExistError as e:
        frappe.log_error(f"Order does not exist: {str(e)}", "Delete Order Error")
        return create_response(NOT_FOUND, "Order item or order does not exist.")
    except Exception as e:
        frappe.log_error(f"Error deleting order or item for user {user_id}: {str(e)}", "Delete Order Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
