import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response


def create_product_review(item_code, user_id, rating, comment):
    try:
        if not (1 <= int(rating) <= 5):
            frappe.throw("Rating must be between 1 and 5.")
        
        product = frappe.get_doc("Products", item_code)
        if not product:
            frappe.throw(f"Product with ID {item_code} does not exist.")
        
        review = frappe.get_doc({
            "doctype": "Product Review",
            "product": item_code,
            "user": user_id,
            "rating": rating,
            "comment": comment,
            "status": "Pending"
        })
        review.insert()
        frappe.db.commit()
        
        # Return success response
        return create_response(SUCCESS, {"message": "Review submitted successfully and is pending approval."})

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error creating product review")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

