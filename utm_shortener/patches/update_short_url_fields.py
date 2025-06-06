import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    """Update Short URL DocType field properties"""
    
    # Update short_code field to not be mandatory on the form level
    # It will still be required in the database but will be auto-generated
    frappe.db.sql("""
        UPDATE `tabDocField` 
        SET reqd = 0, hidden = 0, read_only = 1,
            description = 'Auto-generated unique code for the short URL'
        WHERE parent = 'Short URL' 
        AND fieldname = 'short_code'
    """)
    
    # Update short_url field to be more prominent
    frappe.db.sql("""
        UPDATE `tabDocField` 
        SET bold = 1,
            description = 'Complete short URL that can be shared'
        WHERE parent = 'Short URL' 
        AND fieldname = 'short_url'
    """)
    
    # Update generated_utm_url field description
    frappe.db.sql("""
        UPDATE `tabDocField` 
        SET description = 'Full URL with UTM parameters (if campaign is selected)'
        WHERE parent = 'Short URL' 
        AND fieldname = 'generated_utm_url'
    """)
    
    # Clear cache
    frappe.clear_cache(doctype="Short URL")
    
    print("Short URL field properties updated successfully")