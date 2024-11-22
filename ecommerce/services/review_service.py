import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response


def create_product_review(item_code, username, rating, comment):
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
            "username": username,
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
            WHERE item_code = %s
        """
        
        reviews = frappe.db.sql(query, (item_code,), as_dict=True)

        if not reviews:
            return create_response(SERVER_ERROR, [])

        return create_response(SUCCESS, reviews)

    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching reviews")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def get_average_rating(item_code):
    try:
        if not frappe.db.exists("Products", item_code):
            frappe.throw(f"Product with ID {item_code} does not exist.")

        average_rating = frappe.db.sql("""
            SELECT AVG(rating) as average_rating
            FROM `tabProduct Review`
            WHERE item_code = %s
        """, item_code, as_dict=True)

        return {
            "message": "Average rating fetched successfully.",
            "average_rating": average_rating[0]["average_rating"] if average_rating else 0,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Average Rating Error")
        frappe.throw(f"An error occurred: {str(e)}")
