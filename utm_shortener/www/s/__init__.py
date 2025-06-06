import frappe
from frappe import _

no_cache = 1

def get_context(context):
    """Handle short URL redirects"""
    try:
        # Get the short code from the path
        path_parts = frappe.local.request.path.split('/')
        if len(path_parts) < 3 or path_parts[1] != 's':
            frappe.throw(_("Invalid short URL format"))
        
        short_code = path_parts[2]
        
        # Find the short URL document
        short_url_name = frappe.db.get_value("Short URL", {"short_code": short_code}, "name")
        
        if not short_url_name:
            frappe.throw(_("Short URL not found"), frappe.DoesNotExistError)
        
        # Get the document
        short_url_doc = frappe.get_doc("Short URL", short_url_name)
        
        # Check if URL is active
        if short_url_doc.status != "Active":
            frappe.throw(_("This short URL is not active"))
        
        # Check if URL has expired
        if short_url_doc.is_expired():
            frappe.throw(_("This short URL has expired"))
        
        # Prepare request data for tracking
        request_data = {
            "ip_address": frappe.local.request.remote_addr or "",
            "user_agent": frappe.local.request.headers.get('User-Agent', ''),
            "referrer": frappe.local.request.headers.get('Referer', '')
        }
        
        # Track the click and get redirect URL
        redirect_url = short_url_doc.track_click(request_data)
        
        # Perform redirect
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = redirect_url
        
    except Exception as e:
        frappe.log_error(f"Short URL redirect error: {str(e)}", "Short URL Error")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/404"
