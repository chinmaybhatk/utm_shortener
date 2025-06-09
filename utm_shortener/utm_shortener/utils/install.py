import frappe
import traceback
import json
import os

def before_install():
    """
    Pre-installation checks and logging
    """
    try:
        frappe.log_error("UTM Shortener: Before Install Started")
        
        # Log system information
        log_system_info()
        
        # Validate Frappe environment
        validate_frappe_environment()
        
    except Exception as e:
        frappe.log_error(f"UTM Shortener Pre-Install Error: {str(e)}")
        frappe.log_error(traceback.format_exc())
        raise

def after_install():
    """
    Post-installation setup and verification
    """
    try:
        frappe.log_error("UTM Shortener: After Install Started")
        
        # Create necessary DocTypes
        create_utm_doctypes()
        
        # Setup permissions
        setup_permissions()
        
        # Validate installation
        validate_installation()
        
        frappe.log_error("UTM Shortener: Installation Completed Successfully")
    except Exception as e:
        frappe.log_error(f"UTM Shortener Post-Install Error: {str(e)}")
        frappe.log_error(traceback.format_exc())
        raise

def log_system_info():
    """
    Log detailed system and environment information
    """
    try:
        system_info = {
            "frappe_version": frappe.__version__,
            "python_version": frappe.utils.get_python_version(),
            "installed_apps": frappe.get_installed_apps(),
            "db_name": frappe.conf.get('db_name'),
            "site_name": frappe.local.site
        }
        frappe.log_error(f"System Info: {json.dumps(system_info, indent=2)}")
    except Exception as e:
        frappe.log_error(f"Error logging system info: {str(e)}")

def validate_frappe_environment():
    """
    Check Frappe environment compatibility
    """
    required_apps = ['frappe']
    for app in required_apps:
        if app not in frappe.get_installed_apps():
            raise frappe.ValidationError(f"Required app {app} not installed")

def create_utm_doctypes():
    """
    Ensure UTM related DocTypes exist
    """
    doctypes = [
        {
            "doctype": "DocType",
            "name": "UTM Link",
            "module": "UTM Shortener",
            "fields": [
                {"label": "Original URL", "fieldname": "original_url", "fieldtype": "Data", "reqd": 1},
                {"label": "Short Code", "fieldname": "short_code", "fieldtype": "Data", "unique": 1},
                {"label": "Total Clicks", "fieldname": "total_clicks", "fieldtype": "Int"}
            ]
        },
        {
            "doctype": "DocType",
            "name": "UTM Click Tracking",
            "module": "UTM Shortener",
            "fields": [
                {"label": "UTM Link", "fieldname": "utm_link", "fieldtype": "Link", "options": "UTM Link"},
                {"label": "Clicked At", "fieldname": "clicked_at", "fieldtype": "Datetime"}
            ]
        }
    ]
    
    for doctype_dict in doctypes:
        try:
            if not frappe.db.exists('DocType', doctype_dict['name']):
                doc = frappe.get_doc(doctype_dict)
                doc.insert(ignore_permissions=True)
                frappe.db.commit()
                frappe.log_error(f"Created DocType: {doctype_dict['name']}")
        except Exception as e:
            frappe.log_error(f"Error creating DocType {doctype_dict['name']}: {str(e)}")
            frappe.log_error(traceback.format_exc())

def setup_permissions():
    """
    Setup default permissions for UTM DocTypes
    """
    try:
        # You can add custom permission logic here
        pass
    except Exception as e:
        frappe.log_error(f"Permission Setup Error: {str(e)}")

def validate_installation():
    """
    Final validation checks
    """
    doctypes = ['UTM Link', 'UTM Click Tracking']
    for doctype in doctypes:
        if not frappe.db.exists('DocType', doctype):
            frappe.log_error(f"Validation Failed: DocType {doctype} not found")
            raise frappe.ValidationError(f"Installation incomplete. {doctype} not created.")
    
    frappe.log_error("UTM Shortener: All Validation Checks Passed")