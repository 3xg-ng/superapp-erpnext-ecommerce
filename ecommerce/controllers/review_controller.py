import frappe

from ecommerce.services.review_service import create_product_review, list_reviews

@frappe.whitelist(allow_guest=True)
def get_review(user_id):
    return list_reviews(user_id)


@frappe.whitelist(allow_guest=True)
def add_review(user_id, item_code, rating, comment):
    return create_product_review(user_id, item_code, rating, comment)
