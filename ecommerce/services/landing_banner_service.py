import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_banner_a():
   
    try:
        query = """
            SELECT *
            FROM `tabBannerA`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            raise frappe.DoesNotExistError("No items found!")

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    
    
def get_banner_b():
   
    try:
        query = """
            SELECT *
            FROM `tabBannerB`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            raise frappe.DoesNotExistError("No items found!")

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
    
    
def get_banner_c():
   
    try:
        query = """
            SELECT *
            FROM `tabBannerC`
            WHERE 1=1
        """
         
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            raise frappe.DoesNotExistError("No items found!")

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")