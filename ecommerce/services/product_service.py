import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR
from ecommerce.utils.response_helper import create_response

### Get all items
def list_items(filters=None):
    try:
        query = """
            SELECT item_code, product_name, old_price, new_price, image, rating, color, category, brand, discount
            FROM `tabProducts`
            WHERE 1=1
        """

        params = []

        if filters:
            if filters.get("product_name"):
                query += " AND product_name LIKE %s"
                params.append(f"%{filters['product_name']}%")

            if filters.get("min_price") is not None:
                query += " AND new_price >= %s"
                params.append(filters["min_price"])

            if filters.get("max_price") is not None:
                query += " AND new_price <= %s"
                params.append(filters["max_price"])

            if filters.get("color"):
                query += " AND color = %s"
                params.append(filters["color"])

            if filters.get("category"):
                query += " AND category = %s"
                params.append(filters["category"])

            if filters.get("brand"):
                query += " AND brand = %s"
                params.append(filters["brand"])

            if filters.get("rating"):
                query += " AND rating >= %s"
                params.append(filters["rating"])

            if filters.get("discount"):
                query += " AND discount >= %s"
                params.append(filters["discount"])

        # Execute the query with parameters
        items = frappe.db.sql(query, params, as_dict=True)

        if not items:
            raise frappe.DoesNotExistError("No items found with the specified filters!")

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def list_items_category(limit=8, offset=0, search=None, letter=None, category=None, min_price=None, max_price=None):
    try:
        query = """
            SELECT item_code, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty
            FROM `tabProducts`
            WHERE 1=1
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

        if letter:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"{letter}%", f"{letter}%"])

        if category:
            query += " AND category = %s"
            filters.append(category)

        if min_price is not None:
            query += " AND new_price >= %s"
            filters.append(min_price)
        
        if max_price is not None:
            query += " AND new_price <= %s"
            filters.append(max_price)

        query += " LIMIT %s OFFSET %s"
        filters.extend([limit, offset])
        
        items = frappe.db.sql(query, filters, as_dict=True)

        if not items:
            raise frappe.DoesNotExistError("No items found!")

        # Create the desired response structure
        categories = {}
        collections = {}
        stores = {}  # Assuming you have a separate query for stores

        for item in items:
            # Group by category
            category_name = item['category']
            if category_name not in categories:
                categories[category_name] = {
                    'category': category_name,
                    'products': []
                }
            categories[category_name]['products'].append(item)

            # Group by collection
            collection_name = item['collection']
            if collection_name not in collections:
                collections[collection_name] = {
                    'collection': collection_name,
                    'products': []
                }
            collections[collection_name]['products'].append(item)

        # Convert dict to list
        categories_list = list(categories.values())
        collections_list = list(collections.values())

        # Return final structured response
        return create_response(SUCCESS, {
            'Categories': categories_list,
            'Collections': collections_list,
            'Stores': stores  # Assuming stores are handled elsewhere
        })

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")





### Get single item by code
def get_item_by_code(item_code):
    try:
        item = frappe.get_doc("Products", {"item_code": item_code})

        if not item:
            raise frappe.DoesNotExistError(f"Item with code {item_code} not found!")

        return create_response(SUCCESS, item.as_dict())

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching single item")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")




### Add new item
def add_new_item(item_code, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty):
    
    try:
        if frappe.db.exists("Products", {"item_code": item_code}):
            raise ValueError(f"Item with code '{item_code}' already exists!")

        new_item = frappe.get_doc({
            "doctype": "Products",
            "item_code": item_code,
            "product_name": product_name,
            "category": category,
            "old_price": old_price,
            "new_price": new_price,
            "brand": brand,
            "image": image,
            "rating": rating,
            "description": description,
            "dimension": dimension,
            "display_type": display_type,
            "resolution": resolution,
            "features": features,
            "chipset": chipset,
            "cpu": cpu,
            "internal_memory": internal_memory,
            "ram": ram,
            "battery_type": battery_type,
            "battery_life": battery_life,
            "charging": charging,
            "magsafe_charging": magsafe_charging,
            "color": color,
            "quantity": quantity,
            "availability": availability,
            "collection": collection,
            "model": model,
            "weight": weight,
            "warranty": warranty,
        })

        new_item.insert()
        frappe.db.commit()

        return create_response(SUCCESS, f"Item '{item_code}' added successfully!")

    except ValueError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(f"Error adding new item '{item_code}': {str(e)}", "Add Item Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Update existing item by code
def update_item_by_code(item_code, product_name=None, category=None, old_price=None, new_price=None, image=None, rating=None, brand=None, description=None, product_line=None, model=None, weight=None, availability=None, color=None, quantity=None, warranty=None, collection=None):
    try:
        item = frappe.get_doc("Products", {"item_code": item_code})
        if not item:
            raise frappe.DoesNotExistError(f"Item with code {item_code} not found!")

        attributes = {
            "product_name": product_name,
            "category": category,
            "old_price": old_price,
            "new_price": new_price,
            "rating": rating,
            "image": image,
            "brand": brand,
            "description": description,
            "naming_series": product_line,
            "asset_category": model,
            "weight_per_unit": weight,
            "is_stock_item": availability,
            "color": color,
            "total_projected_qty": quantity,
            "collection": collection,
            "no_of_months_exp": warranty
        }

        for attr, value in attributes.items():
            if value is not None:
                setattr(item, attr, value)

        item.save()
        frappe.db.commit()

        return create_response(SUCCESS, f"Item {item_code} updated successfully!")
    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title=f"Error updating item {item_code}")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Delete item by code
def delete_item_by_code(item_code):
    try:
        if not frappe.db.exists("Products", {"item_code": item_code}):
            raise frappe.DoesNotExistError(f"Item with code {item_code} not found!")

        frappe.delete_doc("Item", item_code)
        frappe.db.commit()

        return create_response(SUCCESS, f"Item {item_code} deleted successfully!")

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title=f"Error deleting item {item_code}")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
