import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def get_category():
    try:
        query = """
            SELECT item_name, category
            FROM `tabProduct Category`
            WHERE 1=1
        """
        
        
        items = frappe.db.sql(query, as_dict=True)

        if not items:
            raise create_response(SERVER_ERROR, [])

        categories = {}

        for item in items:
            category_name = item['category']
            if category_name not in categories:
                categories[category_name] = {
                    'category': category_name,
                    'item': []
                }
            categories[category_name]['item'].append(item)

        categories_list = list(categories.values())

        return create_response(SUCCESS, {
            'Categories': categories_list,
        })

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")