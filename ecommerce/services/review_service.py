import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response


def create_product_review(item_code, user_id, rating, comment):
    try:
        if not (1 <= float(rating) <= 5):
            return create_response(
                BAD_REQUEST, "Rating must be a valid float between 1 and 5."
            )
        
        product = frappe.get_doc(
            "Products", {"item_code": item_code}
        )
        
        if not product:
            return create_response(NOT_FOUND, "Product not found.")
        
        review = frappe.get_doc({
            "doctype": "Product Review",
            "item_code": item_code,
            "user_id": user_id,
            "rating": float(rating), 
            "comment": comment,
            "status": "Pending" 
        })
        review.insert()
        frappe.db.commit()
        
        return create_response(SUCCESS, {"message": "Review submitted successfully and is pending approval."})

    except Exception as e:
        frappe.log_error(message=str(e), title="Error creating product review")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")




def list_reviews(item_code):
    try:
        query = """
            SELECT user_id, rating, comment
            FROM `tabProduct Review`
            WHERE 1=1
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
