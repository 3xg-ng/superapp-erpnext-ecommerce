import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_smartphone_banners():
   
    try:
        query = """
            SELECT *
            FROM `tabSmartphone Banner`
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
    
    

def get_iphone_banners():
   
    try:
        query = """
            SELECT *
            FROM `tabIphone Banner`
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


def get_samsung_banners():
   
    try:
        query = """
            SELECT *
            FROM `tabSamsung Banner`
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
    
    

def get_tecno_banners():
   
    try:
        query = """
            SELECT *
            FROM `tabTecno Banner`
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
    
    

def get_infinix_banners():
   
    try:
        query = """
            SELECT *
            FROM `tabInfinix Banner`
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
    
    

def get_itel_banners():
   
    try:
        query = """
            SELECT *
            FROM `tabItel Banner`
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
    
    
def get_oppo_banners():
   
    try:
        query = """
            SELECT *
            FROM `tabOppo Banner`
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