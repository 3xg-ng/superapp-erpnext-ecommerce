import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_banners():
   
    try:
        query = """
            SELECT *
            FROM `tabShop Banner`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            raise create_response(SERVER_ERROR, [])

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")