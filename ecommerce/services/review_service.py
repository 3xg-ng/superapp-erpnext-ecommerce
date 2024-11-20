import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response


def create_product_review(item_code, user_id, rating, comment):
    try:
        if not (1 <= int(rating) <= 5):
            frappe.throw("Rating must be between 1 and 5.")
        
        product = frappe.db.get_value(
            "Products", 
            {"item_code": item_code},
            as_dict=True
        )
        if not product:
            return create_response(NOT_FOUND, "Product not found.")
        
        review = frappe.get_doc({
            "doctype": "Product Review",
            "item_code": product["item_code"],
            "user_id": user_id,
            "rating": rating,
            "comment": comment,
            "status": "Pending"
        })
        review.insert()
        frappe.db.commit()
        
        return create_response(SUCCESS, {"message": "Review submitted successfully and is pending approval."})

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, f"Product with item_code {item_code} not found.")
    except Exception as e:
        frappe.log_error(message=str(e), title="Error creating product review")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def list_reviews(item_code):
    try:
        query = """
            SELECT *
            FROM `tabProduct Review`
            WHERE item_code = %s
        """
        
        reviews = frappe.db.sql(query, item_code, as_dict=True)

        if not reviews:
            raise create_response(SUCCESS, [])

        return create_response(SUCCESS, reviews)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching reviews")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
