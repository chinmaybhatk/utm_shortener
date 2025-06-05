import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    """Add base_url and full_url fields to UTM Campaign DocType"""
    
    # Check if fields already exist
    if not frappe.db.exists("Custom Field", {"dt": "UTM Campaign", "fieldname": "base_url"}):
        # Add Base URL field
        create_custom_field("UTM Campaign", {
            "fieldname": "base_url",
            "label": "Base URL",
            "fieldtype": "Data",
            "insert_after": "utm_content",
            "description": "Enter the base URL without UTM parameters (e.g., https://example.com/page)",
            "length": 500
        })
    
    if not frappe.db.exists("Custom Field", {"dt": "UTM Campaign", "fieldname": "full_url"}):
        # Add Full URL field (Read Only)
        create_custom_field("UTM Campaign", {
            "fieldname": "full_url",
            "label": "Full URL with UTM Parameters",
            "fieldtype": "Small Text",
            "insert_after": "base_url",
            "read_only": 1,
            "description": "Auto-generated URL with all UTM parameters"
        })
    
    if not frappe.db.exists("Custom Field", {"dt": "UTM Campaign", "fieldname": "copy_url_button"}):
        # Add Copy URL button
        create_custom_field("UTM Campaign", {
            "fieldname": "copy_url_button",
            "label": "Copy URL",
            "fieldtype": "Button",
            "insert_after": "full_url",
            "depends_on": "eval:doc.full_url"
        })
    
    # Commit changes
    frappe.db.commit()
    
    print("UTM Campaign URL fields added successfully")
