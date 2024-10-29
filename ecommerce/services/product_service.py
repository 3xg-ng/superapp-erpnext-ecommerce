import frappe
from ecommerce.constants.http_status import SUCCESS, NOT_FOUND, SERVER_ERROR, BAD_REQUEST
from ecommerce.utils.response_helper import create_response

### Get all items
def list_items(limit=50, offset=0, search=None, name=None, category=None, min_price=None, max_price=None, color=None, brand=None, rating=None, sort=None):
    try:
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE 1=1
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

        if name:
            query += " AND (product_name LIKE %s)"
            filters.append(f"{name}%")

        if category:
            query += " AND category = %s"
            filters.append(category)

        if min_price is not None:
            query += " AND new_price >= %s"
            filters.append(min_price)
        
        if max_price is not None:
            query += " AND new_price <= %s"
            filters.append(max_price)

        if color:
            query += " AND color = %s"
            filters.append(color)

        if brand:
            query += " AND brand = %s"
            filters.append(brand)
            
        if rating:
            query += " AND rating = %s"
            filters.append(rating)

        if sort:
            if sort == "popular":
                query += " ORDER BY total_projected_qty DESC"
            elif sort == "newest":
                query += " ORDER BY creation_date DESC"
            elif sort == "highest_to_lowest":
                query += " ORDER BY new_price DESC" 
            elif sort == "lowest_to_highest":
                query += " ORDER BY new_price ASC"
        else:
            query += " ORDER BY product_name ASC"

        query += " LIMIT %s OFFSET %s"
        filters.extend([limit, offset])

        items = frappe.db.sql(query, filters, as_dict=True)

        if not items:
            raise frappe.DoesNotExistError("No items found!")

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



def list_items_category(limit=8, offset=0, search=None, letter=None, category=None, min_price=None, max_price=None):
    try:
        query = """
            SELECT product_id, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty
            FROM `tabProducts`
            WHERE 1=1
        """
        
        filters = []
        
        # General search for item name or description
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

        # Search for items that start with a specific letter
        if letter:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"{letter}%", f"{letter}%"])

        # Filter by category
        if category:
            query += " AND category = %s"
            filters.append(category)

        # Price range filters
        if min_price is not None:
            query += " AND new_price >= %s"
            filters.append(min_price)
        
        if max_price is not None:
            query += " AND new_price <= %s"
            filters.append(max_price)

        # Limit and offset
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



### Get items by Smartphone category
def list_items_smartphone(limit=50, offset=0, search=None, category=None, min_price=None, max_price=None):
   
    try:
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE category="Smartphones"
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

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

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

    

### Get items by Accessories category
def list_items_accessories(limit=50, offset=0, search=None, category=None, min_price=None, max_price=None):
   
    try:
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE category="Accessories"
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

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

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Get items by Laptops category
def list_items_laptops(limit=50, offset=0, search=None, category=None, min_price=None, max_price=None):
   
    try:
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE category="Laptops"
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

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

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")




### Get items by Home Appliance category
def list_items_home_appliance(limit=50, offset=0, search=None, category=None, min_price=None, max_price=None):
   
    try:
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE category="Home Appliance"
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

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

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

    

### Get items by Kiddies category
def list_items_kiddies(limit=50, offset=0, search=None, category=None, min_price=None, max_price=None):
   
    try:
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE category="Kiddies"
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

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

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")

    

### Get items by New Arrival category
def list_items_new_arrival(limit=50, offset=0, search=None, category=None, min_price=None, max_price=None):
   
    try:
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE collection="New Arrival"
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

        if category:
            query += " AND collection = %s"
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

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Get items by New Arrival category
def list_items_official_store(limit=50, offset=0, search=None, category=None, min_price=None, max_price=None):
   
    try:
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE collection="Official Store"
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

        if category:
            query += " AND collection = %s"
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

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Get items by New Arrival category
def list_items_best_seller(limit=50, offset=0, search=None, category=None, min_price=None, max_price=None):
   
    try:
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE collection="Best Seller"
        """
        
        filters = []
        
        if search:
            query += " AND (product_name LIKE %s OR description LIKE %s)"
            filters.extend([f"%{search}%", f"%{search}%"])

        if category:
            query += " AND collection = %s"
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

        return create_response(SUCCESS, items)

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching items")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Get single item by code
def get_product_by_id():
    try:
        # Log form_dict to inspect received parameters
        frappe.log_error(message=f"form_dict content: {frappe.form_dict}", title="Debug: form_dict Inspection")

        # Retrieve the product_id from request parameters or JSON body
        product_id = frappe.form_dict.get("product_id")

        if not product_id:
            raise ValueError("Product ID is required.")

        # Define the SQL query to fetch a product by its ID
        query = """
            SELECT *
            FROM `tabProducts`
            WHERE product_id = %s
        """

        # Execute the query with product_id as a parameter
        product = frappe.db.sql(query, (product_id,), as_dict=True)

        if not product:
            raise frappe.DoesNotExistError(f"Product with ID {product_id} not found!")

        return create_response(SUCCESS, product[0])

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except ValueError as e:
        return create_response(BAD_REQUEST, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title="Error fetching product by ID")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")






### Add new item
def add_new_item(product_id, product_name, category, old_price, new_price, image, rating, brand, description, dimension, display_type, resolution, features, chipset, cpu, internal_memory, ram, battery_type, battery_life, charging, magsafe_charging, collection, model, weight, availability, color, quantity, warranty):
    
    try:
        if frappe.db.exists("Item", {"product_id": product_id}):
            raise ValueError(f"Item with code '{product_id}' already exists!")

        new_item = frappe.get_doc({
            "doctype": "Products",
            "product_id": product_id,
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

        return create_response(SUCCESS, f"Item '{product_id}' added successfully!")

    except ValueError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(f"Error adding new item '{product_id}': {str(e)}", "Add Item Error")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Update existing item by code
def update_item_by_code(product_id, product_name=None, category=None, old_price=None, new_price=None, image=None, rating=None, brand=None, description=None, product_line=None, model=None, weight=None, availability=None, color=None, quantity=None, warranty=None, collection=None):
    try:
        item = frappe.get_doc("Item", {"product_id": product_id})
        if not item:
            raise frappe.DoesNotExistError(f"Item with code {product_id} not found!")

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

        return create_response(SUCCESS, f"Item {product_id} updated successfully!")
    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title=f"Error updating item {product_id}")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")



### Delete item by code
def delete_item_by_code(product_id):
    try:
        if not frappe.db.exists("Item", {"product_id": product_id}):
            raise frappe.DoesNotExistError(f"Item with code {product_id} not found!")

        frappe.delete_doc("Item", product_id)
        frappe.db.commit()

        return create_response(SUCCESS, f"Item {product_id} deleted successfully!")

    except frappe.DoesNotExistError as e:
        return create_response(NOT_FOUND, str(e))
    except Exception as e:
        frappe.log_error(message=str(e), title=f"Error deleting item {product_id}")
        return create_response(SERVER_ERROR, f"An unexpected error occurred: {str(e)}")
